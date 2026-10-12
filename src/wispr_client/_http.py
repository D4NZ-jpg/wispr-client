"""Tiny typed HTTP helper on the standard library (no extra dependency for a handful of JSON calls)."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel, ValidationError

from .errors import ApiError

if TYPE_CHECKING:
    from collections.abc import Mapping

_log = logging.getLogger(__name__)
M = TypeVar("M", bound=BaseModel)

USER_AGENT = "wispr-client/0.1 (+unofficial)"


def request_json(
    method: str,
    url: str,
    model: type[M],
    *,
    headers: Mapping[str, str] | None = None,
    body: Mapping[str, Any] | None = None,
    timeout: float,
) -> M:
    """Send a JSON request and validate the JSON response into *model*.

    Raises :class:`ApiError` with the HTTP status on any non-2xx response or invalid payload.
    """
    if not url.startswith("https://"):
        raise ApiError(f"refusing non-HTTPS URL: {url}")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method.upper())  # noqa: S310 (scheme checked)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", USER_AGENT)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    for key, value in (headers or {}).items():
        req.add_header(key, value)

    _log.debug("%s %s", method.upper(), url.split("?", maxsplit=1)[0])
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            payload = resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:300]
        raise ApiError(
            f"{method.upper()} {url.split('?', maxsplit=1)[0]} -> HTTP {exc.code}: {detail}", exc.code
        ) from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ApiError(f"{method.upper()} {url.split('?', maxsplit=1)[0]} failed: {exc}") from exc

    try:
        parsed = json.loads(payload)
        if isinstance(parsed, dict) and isinstance(parsed.get("data"), dict) and len(parsed) <= 3:
            parsed = parsed["data"]  # some Wispr endpoints wrap results in {"data": ...}
        return model.model_validate(parsed)
    except (ValueError, ValidationError) as exc:
        raise ApiError(f"unexpected response from {url.split('?', maxsplit=1)[0]}: {exc}") from exc
