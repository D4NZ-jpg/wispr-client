from __future__ import annotations

from typing import Any

import pytest

from wispr_client import auth as auth_mod
from wispr_client.auth import Authenticator, TokenStore
from wispr_client.config import WisprSettings
from wispr_client.errors import ApiError, AuthError, NotLoggedInError
from wispr_client.models import SupabaseTokenResponse, TokenSet

from .conftest import make_jwt


def test_not_logged_in(settings: WisprSettings) -> None:
    with pytest.raises(NotLoggedInError):
        Authenticator(settings).access_token()


def test_fresh_token_is_not_refreshed(auth: Authenticator, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(auth_mod, "request_json", lambda *a, **k: pytest.fail("unexpected refresh"))
    assert auth.access_token() == auth.current().access_token.get_secret_value()


def test_expiring_token_refreshes_and_persists(
    settings: WisprSettings, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = TokenStore(settings.token_file)
    store.save(
        TokenSet.from_tokens(make_jwt(exp_in=30), "old-refresh", first_name="Dan", wispr_user_id="uuid-1")
    )
    new_access = make_jwt(exp_in=7200)
    calls: list[dict[str, Any]] = []

    def fake_request(method: str, url: str, model: type[Any], **kw: Any) -> Any:
        calls.append({"url": url, **kw})
        assert model is SupabaseTokenResponse
        return SupabaseTokenResponse(access_token=new_access, refresh_token="new-refresh")

    monkeypatch.setattr(auth_mod, "request_json", fake_request)
    token = Authenticator(settings, store).access_token()

    assert token == new_access
    assert calls[0]["body"] == {"refresh_token": "old-refresh"}
    assert calls[0]["headers"]["apikey"] == settings.supabase_anon_key
    saved = store.load()
    assert saved is not None
    assert saved.refresh_token.get_secret_value() == "new-refresh"
    assert saved.first_name == "Dan"  # profile fields preserved
    assert saved.wispr_user_id == "uuid-1"


def test_refresh_failure_is_auth_error(settings: WisprSettings, monkeypatch: pytest.MonkeyPatch) -> None:
    store = TokenStore(settings.token_file)
    store.save(TokenSet.from_tokens(make_jwt(exp_in=30), "dead"))

    def boom(*_: Any, **__: Any) -> Any:
        raise ApiError("HTTP 400: invalid refresh token", 400)

    monkeypatch.setattr(auth_mod, "request_json", boom)
    with pytest.raises(AuthError, match="wispr login"):
        Authenticator(settings, store).access_token()


def test_refresh_rereads_store_under_lock(settings: WisprSettings, monkeypatch: pytest.MonkeyPatch) -> None:
    """If another process refreshed meanwhile, the single-use refresh token must not be spent twice."""
    store = TokenStore(settings.token_file)
    store.save(TokenSet.from_tokens(make_jwt(exp_in=7200), "already-rotated"))
    monkeypatch.setattr(auth_mod, "request_json", lambda *a, **k: pytest.fail("double refresh"))
    assert Authenticator(settings, store).refresh().refresh_token.get_secret_value() == "already-rotated"


def test_logout(auth: Authenticator) -> None:
    assert auth.logout() is True
    assert auth.logout() is False
    with pytest.raises(NotLoggedInError):
        auth.current()
