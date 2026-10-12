"""Runtime settings, overridable through ``WISPR_*`` environment variables."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_home() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config"
    return Path(base) / "wispr-client"


# Public Supabase "anon" key shipped in the Wispr Flow desktop app. It identifies the
# project for token refresh; it is not a user secret.
_SUPABASE_ANON_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRvZGprZnFod3J6cWp3a2Zud"
    "GhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTk4ODQzMDcsImV4cCI6MjAzNTQ2MDMwN30."
    "h6EeQ_6kqFeznH25icVUX0Szn9__kc8HoSXAsxxBWG8"
)

Platform = Literal["PLATFORM_WIN32", "PLATFORM_MACOS"]


class WisprSettings(BaseSettings):
    """Endpoints and client identity. Defaults mirror Wispr Flow 1.6.1102 for Windows."""

    model_config = SettingsConfigDict(env_prefix="WISPR_", frozen=True, extra="ignore")

    home: Path = Field(default_factory=_default_home, description="Directory holding tokens.json")
    api_base: HttpUrl = HttpUrl("https://api.wisprflow.ai")
    login_base: HttpUrl = HttpUrl("https://wisprflow.ai")
    grpc_host: str = "inference.wisprflow.com:443"
    grpc_tls: bool = Field(default=True, description="Disable only for a local test server")
    model_id: str = "v31pl413"
    supabase_url: HttpUrl = HttpUrl("https://dodjkfqhwrzqjwkfnthl.supabase.co")
    supabase_anon_key: str = _SUPABASE_ANON_KEY
    workos_api: HttpUrl = HttpUrl("https://api.workos.com")

    client_name: str = "Wispr Flow"
    client_version: str = "1.6.1102"
    platform: Platform = "PLATFORM_WIN32"

    http_timeout_s: float = Field(default=15.0, gt=0)
    stream_timeout_s: float = Field(default=600.0, gt=0, description="Hard cap on one dictation stream")
    refresh_skew_s: int = Field(default=300, ge=0, description="Refresh tokens this long before expiry")

    @property
    def token_file(self) -> Path:
        return self.home / "tokens.json"

    @property
    def version_tuple(self) -> tuple[int, int, int]:
        major, minor, patch = (int(p) for p in (*self.client_version.split("."), "0", "0")[:3])
        return major, minor, patch


@lru_cache(maxsize=1)
def get_settings() -> WisprSettings:
    """Process-wide settings instance (environment read once)."""
    return WisprSettings()
