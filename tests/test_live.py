"""Real-service checks. Opt in with ``pytest -m live`` after ``wispr login``; each run uses ~2 dictations."""

from __future__ import annotations

import math
import struct

import pytest

from wispr_client import Authenticator, TranscriptionClient, WisprApi, WisprSettings

pytestmark = pytest.mark.live


@pytest.fixture(scope="module")
def live_auth() -> Authenticator:
    auth = Authenticator(WisprSettings())
    if auth.store.load() is None:
        pytest.skip("not logged in; run `wispr login`")
    return auth


def test_profile(live_auth: Authenticator) -> None:
    assert WisprApi(live_auth).profile().user_id == live_auth.current().user_id


def test_tone_is_not_speech(live_auth: Authenticator) -> None:
    """A 1 s 440 Hz tone round-trips through the real stream and yields (near-)empty text."""
    tone = b"".join(
        struct.pack("<h", int(3000 * math.sin(2 * math.pi * 440 * i / 16000))) for i in range(16000)
    )
    result = TranscriptionClient(live_auth).transcribe_pcm(tone, language="en")
    assert len(result.text) < 40
