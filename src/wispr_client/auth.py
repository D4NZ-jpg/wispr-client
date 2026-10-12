"""Session storage, device-code login and automatic token refresh."""

from __future__ import annotations

import contextlib
import logging
import os
import re
import sys
import tempfile
import time
import uuid
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlencode

from ._http import request_json
from .config import WisprSettings, get_settings
from .errors import ApiError, AuthError, NotLoggedInError
from .models import DevicePollResponse, JwtClaims, SupabaseTokenResponse, TokenSet, WorkosTokenResponse

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

_log = logging.getLogger(__name__)

if sys.platform == "win32":
    import msvcrt

    def _lock_fd(fd: int) -> None:
        msvcrt.locking(fd, msvcrt.LK_LOCK, 1)

    def _unlock_fd(fd: int) -> None:
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)

else:
    import fcntl

    def _lock_fd(fd: int) -> None:
        fcntl.flock(fd, fcntl.LOCK_EX)

    def _unlock_fd(fd: int) -> None:
        fcntl.flock(fd, fcntl.LOCK_UN)


_WORKOS_CLIENT_RE = re.compile(r"(client_[A-Za-z0-9]+)")


class TokenStore:
    """``tokens.json`` (mode 0600) plus a sibling lock file serialising refreshes across processes."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock_path = path.with_suffix(".lock")

    def load(self) -> TokenSet | None:
        try:
            raw = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        return TokenSet.model_validate_json(raw)

    def save(self, tokens: TokenSet) -> None:
        """Atomically replace the token file, never leaving it world-readable."""
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, prefix=".tokens.", suffix=".tmp")
        tmp_path = Path(tmp)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(tokens.dump_secrets())
            tmp_path.chmod(0o600)
            tmp_path.replace(self.path)
        except BaseException:
            tmp_path.unlink(missing_ok=True)
            raise

    def clear(self) -> bool:
        existed = self.path.exists()
        self.path.unlink(missing_ok=True)
        return existed

    @contextlib.contextmanager
    def locked(self) -> Iterator[None]:
        self._lock_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd = os.open(self._lock_path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            _lock_fd(fd)
            yield
        finally:
            with contextlib.suppress(OSError):
                _unlock_fd(fd)
            os.close(fd)


class Authenticator:
    """Hands out a valid access token, refreshing (and persisting) it when close to expiry."""

    def __init__(self, settings: WisprSettings | None = None, store: TokenStore | None = None) -> None:
        self.settings = settings or get_settings()
        self.store = store or TokenStore(self.settings.token_file)

    # ------------------------------------------------------------------ public API

    def current(self) -> TokenSet:
        tokens = self.store.load()
        if tokens is None:
            raise NotLoggedInError(f"not logged in (no {self.store.path}); run `wispr login`")
        return tokens

    def access_token(self) -> str:
        """A token valid for at least ``refresh_skew_s`` seconds."""
        tokens = self.current()
        if tokens.expires_within(self.settings.refresh_skew_s):
            tokens = self.refresh()
        return tokens.access_token.get_secret_value()

    def refresh(self, *, force: bool = False) -> TokenSet:
        """Refresh under the cross-process lock. Re-reads first: another process may have just refreshed
        (refresh tokens are single-use, so refreshing twice would log us out)."""
        with self.store.locked():
            tokens = self.current()
            if not force and not tokens.expires_within(self.settings.refresh_skew_s):
                return tokens
            _log.info("refreshing %s session (expires %s)", tokens.provider, tokens.expires_at.isoformat())
            access, refresh = self._refresh_with_provider(tokens)
            updated = TokenSet.from_tokens(
                access,
                refresh,
                first_name=tokens.first_name,
                last_name=tokens.last_name,
                workos_client_id=tokens.workos_client_id,
            )
            self.store.save(updated)
            return updated

    def login_device_code(
        self,
        on_url: Callable[[str], None],
        *,
        timeout_s: float = 600.0,
        poll_interval_s: float = 3.0,
    ) -> TokenSet:
        """Browser login exactly like the desktop app: show a URL, poll until the user signs in."""
        device_code = str(uuid.uuid4())
        query = urlencode(
            {
                "device_code": device_code,
                "auto_signin": "true",
                "skip_default_trial": "true",
                "grant_weekly_bonus": "true",
                "workos_capable": "true",
            }
        )
        on_url(f"{str(self.settings.login_base).rstrip('/')}/login?{query}")

        poll_url = (
            f"{str(self.settings.api_base).rstrip('/')}/device/poll?{urlencode({'device_code': device_code})}"
        )
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            time.sleep(poll_interval_s)
            try:
                resp = request_json("GET", poll_url, DevicePollResponse, timeout=self.settings.http_timeout_s)
            except ApiError as exc:
                if exc.status in (None, 404, 425, 429) or (exc.status or 0) >= 500:
                    _log.debug("device poll not ready: %s", exc)
                    continue
                raise AuthError(f"device login failed: {exc}") from exc
            if resp.status == "timeout":
                raise AuthError("device login timed out on the server; run `wispr login` again")
            if resp.complete and resp.access_token and resp.refresh_token:
                claims = JwtClaims.decode(resp.access_token)
                tokens = TokenSet.from_tokens(
                    resp.access_token,
                    resp.refresh_token,
                    first_name=resp.first_name,
                    last_name=resp.last_name,
                    workos_client_id=_workos_client_id(claims),
                )
                with self.store.locked():
                    self.store.save(tokens)
                return tokens
        raise AuthError(f"no login completed within {timeout_s:.0f}s")

    def logout(self) -> bool:
        with self.store.locked():
            return self.store.clear()

    # ------------------------------------------------------------------ providers

    def _refresh_with_provider(self, tokens: TokenSet) -> tuple[str, str]:
        refresh_token = tokens.refresh_token.get_secret_value()
        try:
            if tokens.provider == "supabase":
                s = request_json(
                    "POST",
                    f"{str(self.settings.supabase_url).rstrip('/')}/auth/v1/token?grant_type=refresh_token",
                    SupabaseTokenResponse,
                    headers={"apikey": self.settings.supabase_anon_key},
                    body={"refresh_token": refresh_token},
                    timeout=self.settings.http_timeout_s,
                )
                return s.access_token, s.refresh_token
            client_id = tokens.workos_client_id
            if not client_id:
                raise AuthError("WorkOS session without a client id; run `wispr login` again")
            w = request_json(
                "POST",
                f"{str(self.settings.workos_api).rstrip('/')}/user_management/authenticate",
                WorkosTokenResponse,
                body={"grant_type": "refresh_token", "client_id": client_id, "refresh_token": refresh_token},
                timeout=self.settings.http_timeout_s,
            )
            return w.access_token, w.refresh_token
        except ApiError as exc:
            raise AuthError(f"token refresh failed ({exc}); run `wispr login` again") from exc


def _workos_client_id(claims: JwtClaims) -> str | None:
    if claims.provider != "workos":
        return None
    match = _WORKOS_CLIENT_RE.search(claims.iss)
    return match.group(1) if match else None
