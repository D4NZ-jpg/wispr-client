"""Exception hierarchy. Everything raised by this package derives from :class:`WisprError`."""

from __future__ import annotations


class WisprError(Exception):
    """Base class for wispr-client errors."""


class NotLoggedInError(WisprError):
    """No stored session. Run ``wispr login``."""


class AuthError(WisprError):
    """The session could not be refreshed or was rejected; ``wispr login`` again."""


class AudioError(WisprError):
    """Input audio could not be read or converted (missing ffmpeg, bad file, ...)."""


class ApiError(WisprError):
    """A REST call failed."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class TranscriptionError(WisprError):
    """The dictation stream failed or returned no result."""

    def __init__(self, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code
