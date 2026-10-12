"""Authenticated REST calls to ``api.wisprflow.ai``.

Note the header format: Wispr's REST API takes the raw access token, *without* ``Bearer``.
"""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

from ._http import request_json
from .auth import Authenticator
from .errors import ApiError
from .models import UserProfile

M = TypeVar("M", bound=BaseModel)


class WisprApi:
    def __init__(self, auth: Authenticator | None = None) -> None:
        self.auth = auth or Authenticator()

    def request(self, method: str, path: str, model: type[M], *, body: dict[str, Any] | None = None) -> M:
        """Call *path* and validate the response, retrying once with a forced refresh on HTTP 401."""
        url = f"{str(self.auth.settings.api_base).rstrip('/')}/{path.lstrip('/')}"
        for attempt in range(2):
            token = self.auth.access_token() if attempt == 0 else self._forced_token()
            try:
                return request_json(
                    method,
                    url,
                    model,
                    headers={"Authorization": token},
                    body=body,
                    timeout=self.auth.settings.http_timeout_s,
                )
            except ApiError as exc:
                if exc.status != 401 or attempt:
                    raise
        raise AssertionError("unreachable")  # pragma: no cover

    def profile(self) -> UserProfile:
        return self.request("GET", "/api/v1/user/profile", UserProfile)

    def _forced_token(self) -> str:
        return self.auth.refresh(force=True).access_token.get_secret_value()
