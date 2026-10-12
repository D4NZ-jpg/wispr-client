from __future__ import annotations

import stat
import wave
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import SecretStr

from wispr_client.audio import PACKET_BYTES, Packetizer, load_pcm
from wispr_client.errors import AudioError
from wispr_client.languages import from_wispr_language, to_wispr_language
from wispr_client.models import (
    STREAM_EVENT_ADAPTER,
    FinalEvent,
    JwtClaims,
    PartialEvent,
    TokenSet,
    TranscriptionResult,
)

from .conftest import make_jwt


@pytest.mark.parametrize(
    ("hint", "expected"),
    [
        ("en", "LANGUAGE_ENGLISH_US"),
        ("en-GB", "LANGUAGE_ENGLISH_UK"),
        ("en_ca", "LANGUAGE_ENGLISH_CA"),
        ("pt-BR", "LANGUAGE_PORTUGUESE"),
        ("zh-TW", "LANGUAGE_CHINESE_TRADITIONAL"),
        ("es", "LANGUAGE_SPANISH"),
        ("LANGUAGE_FRENCH", "LANGUAGE_FRENCH"),
        ("", None),
        (None, None),
        ("auto", None),
        ("xx", None),
    ],
)
def test_to_wispr_language(hint: str | None, expected: str | None) -> None:
    assert to_wispr_language(hint) == expected


def test_from_wispr_language() -> None:
    assert from_wispr_language("LANGUAGE_ENGLISH_US") == "en"
    assert from_wispr_language("LANGUAGE_ENGLISH_UK") == "en-GB"
    assert from_wispr_language("LANGUAGE_SPANISH") == "es"


def test_packetizer_splits_and_pads() -> None:
    p = Packetizer()
    assert p.feed(b"\x01" * (PACKET_BYTES - 10)) == []
    packets = p.feed(b"\x02" * 20)  # buffer now PACKET_BYTES + 10
    assert packets == [b"\x01" * (PACKET_BYTES - 10) + b"\x02" * 10]
    tail = p.flush()
    assert tail == [b"\x02" * 10 + b"\x00" * (PACKET_BYTES - 10)]
    assert p.flush() == []


def test_load_pcm_native_wav_and_raw(tmp_path: Path) -> None:
    pcm = b"\x01\x00" * 1600
    wav_path = tmp_path / "a.wav"
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(pcm)
    assert load_pcm(wav_path) == pcm
    raw = tmp_path / "a.raw"
    raw.write_bytes(pcm + b"\x07")  # odd byte dropped
    assert load_pcm(raw) == pcm


def test_load_pcm_missing_file(tmp_path: Path) -> None:
    with pytest.raises(AudioError, match="no such audio file"):
        load_pcm(tmp_path / "nope.ogg")


def test_jwt_claims_and_tokenset() -> None:
    token = make_jwt("abc", exp_in=60, iss="https://api.workos.com/user_management/client_01XYZ")
    claims = JwtClaims.decode(token)
    assert claims.provider == "workos"
    ts = TokenSet.from_tokens(token, "r")
    assert ts.user_id == "abc"
    assert ts.expires_within(300)
    assert not ts.expires_within(0)
    assert "r'" not in repr(ts)  # secrets masked
    assert isinstance(ts.access_token, SecretStr)
    with pytest.raises(ValueError, match="not a JWT"):
        JwtClaims.decode("garbage")


def test_tokenset_roundtrip_keeps_secrets() -> None:
    ts = TokenSet.from_tokens(make_jwt(), "refresh-xyz")
    again = TokenSet.model_validate_json(ts.dump_secrets())
    assert again.refresh_token.get_secret_value() == "refresh-xyz"
    assert again.expires_at - datetime.now(UTC) > timedelta(minutes=50)


def test_stream_event_contract() -> None:
    result = TranscriptionResult(text="hi", request_id="r1", status="formatted", languages=("en",))
    for event in (PartialEvent(text="h"), FinalEvent(result=result)):
        parsed = STREAM_EVENT_ADAPTER.validate_json(event.model_dump_json())
        assert parsed == event
    assert '"v":1' in FinalEvent(result=result).model_dump_json()


def test_token_file_is_private(auth: object, tmp_path: Path) -> None:
    mode = stat.S_IMODE((tmp_path / "tokens.json").stat().st_mode)
    assert mode == 0o600
