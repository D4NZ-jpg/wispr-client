"""Unofficial, typed Python client for Wispr Flow speech-to-text.

>>> from wispr_client import TranscriptionClient
>>> TranscriptionClient().transcribe_file(Path("note.ogg"), language="en").text
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from .api import WisprApi
from .auth import Authenticator, TokenStore
from .config import WisprSettings, get_settings
from .errors import ApiError, AudioError, AuthError, NotLoggedInError, TranscriptionError, WisprError
from .models import (
    STREAM_EVENT_ADAPTER,
    ErrorEvent,
    FinalEvent,
    PartialEvent,
    StreamEvent,
    TokenSet,
    TranscriptionResult,
    UserProfile,
)
from .transcribe import StreamSession, TranscriptionClient

try:
    __version__ = version("wispr-client")
except PackageNotFoundError:  # running from a source checkout
    __version__ = "0.0.0+local"

__all__ = [
    "STREAM_EVENT_ADAPTER",
    "ApiError",
    "AudioError",
    "AuthError",
    "Authenticator",
    "ErrorEvent",
    "FinalEvent",
    "NotLoggedInError",
    "PartialEvent",
    "StreamEvent",
    "StreamSession",
    "TokenSet",
    "TokenStore",
    "TranscriptionClient",
    "TranscriptionError",
    "TranscriptionResult",
    "UserProfile",
    "WisprApi",
    "WisprError",
    "WisprSettings",
    "__version__",
    "get_settings",
]
