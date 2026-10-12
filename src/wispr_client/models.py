"""Typed data models (pydantic v2).

* Wire models (``*Response``) validate what Wispr/Supabase send; unknown fields are ignored.
* Domain models (``TokenSet``, ``TranscriptionResult``) are frozen.
* ``StreamEvent`` is the versioned JSON-lines contract of ``wispr stream`` / ``wispr transcribe --json``,
  consumed by integrations such as the Hermes plugin.
"""

from __future__ import annotations

import base64
import json
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, SecretStr, TypeAdapter

AuthProvider = Literal["supabase", "workos"]
ResultStatus = Literal["formatted", "raw_transcript", "error", "unspecified"]


class _Wire(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)


class _Frozen(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


# --------------------------------------------------------------------------- auth


class JwtClaims(_Wire):
    """The subset of access-token claims we rely on. Signature is NOT verified (server does that)."""

    sub: str
    exp: int
    iss: str = ""
    email: str | None = None
    session_id: str | None = None

    @classmethod
    def decode(cls, token: str) -> JwtClaims:
        try:
            payload = token.split(".")[1]
            raw = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
            return cls.model_validate(json.loads(raw))
        except (IndexError, ValueError) as exc:
            raise ValueError("access token is not a JWT") from exc

    @property
    def provider(self) -> AuthProvider:
        return "workos" if "workos" in self.iss else "supabase"

    @property
    def expires_at(self) -> datetime:
        return datetime.fromtimestamp(self.exp, tz=UTC)


class TokenSet(_Frozen):
    """A stored session. Secrets are ``SecretStr`` so they never appear in reprs or logs."""

    access_token: SecretStr
    refresh_token: SecretStr
    provider: AuthProvider
    user_id: str
    expires_at: datetime
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    workos_client_id: str | None = None
    obtained_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def from_tokens(cls, access_token: str, refresh_token: str, **extra: Any) -> TokenSet:
        """Build from raw tokens, deriving identity and expiry from the JWT claims."""
        claims = JwtClaims.decode(access_token)
        return cls(
            access_token=SecretStr(access_token),
            refresh_token=SecretStr(refresh_token),
            provider=claims.provider,
            user_id=claims.sub,
            expires_at=claims.expires_at,
            email=extra.pop("email", None) or claims.email,
            **extra,
        )

    def expires_within(self, seconds: float) -> bool:
        return self.expires_at - datetime.now(UTC) <= timedelta(seconds=seconds)

    def dump_secrets(self) -> str:
        """JSON including secret values (for the private token file only)."""
        data = self.model_dump(mode="json")
        data["access_token"] = self.access_token.get_secret_value()
        data["refresh_token"] = self.refresh_token.get_secret_value()
        return json.dumps(data, indent=2)


class DevicePollResponse(_Wire):
    """``GET /device/poll`` and the ``/device/stream`` SSE payload."""

    status: str
    access_token: str | None = None
    refresh_token: str | None = None
    provider: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    @property
    def complete(self) -> bool:
        return self.status == "complete" and bool(self.access_token and self.refresh_token)


class SupabaseTokenResponse(_Wire):
    access_token: str
    refresh_token: str
    expires_at: int | None = None


class WorkosTokenResponse(_Wire):
    access_token: str
    refresh_token: str


class UserProfile(_Wire):
    """``GET /api/v1/user/profile``."""

    user_id: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None


# --------------------------------------------------------------------------- transcription


class TranscriptionResult(_Frozen):
    text: str
    raw_text: str = ""
    languages: tuple[str, ...] = ()
    status: ResultStatus = "unspecified"
    confidence: float | None = None
    audio_seconds: float | None = None
    origin: str | None = None
    request_id: str


# --------------------------------------------------------------------------- CLI JSON contract

EVENT_SCHEMA_VERSION: Literal[1] = 1


class _Event(_Frozen):
    v: Literal[1] = EVENT_SCHEMA_VERSION


class PartialEvent(_Event):
    type: Literal["partial"] = "partial"
    text: str


class FinalEvent(_Event):
    type: Literal["final"] = "final"
    result: TranscriptionResult


class ErrorEvent(_Event):
    type: Literal["error"] = "error"
    error: str
    kind: str = Field(description="Exception class name, e.g. AuthError")


StreamEvent = Annotated[PartialEvent | FinalEvent | ErrorEvent, Field(discriminator="type")]
STREAM_EVENT_ADAPTER: TypeAdapter[StreamEvent] = TypeAdapter(StreamEvent)
