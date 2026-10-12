from __future__ import annotations

import io
import json
import os
from pathlib import Path

import pytest

from wispr_client import cli
from wispr_client._proto import flow_api_v1_pb2 as pb
from wispr_client.auth import Authenticator
from wispr_client.errors import TranscriptionError
from wispr_client.models import STREAM_EVENT_ADAPTER, FinalEvent, PartialEvent, TokenSet
from wispr_client.transcribe import TranscriptionClient

from .conftest import FakeWispr, make_jwt


def test_transcribe_pcm_protocol(
    auth: Authenticator, fake_server: tuple[FakeWispr, str], pcm_1s: bytes
) -> None:
    fake, _ = fake_server
    result = TranscriptionClient(auth, app_name="Test").transcribe_pcm(
        pcm_1s, language="en", vocabulary=["Hermes"]
    )

    assert result.text == "Hello from the fake server."
    assert result.status == "formatted"
    assert result.languages == ("en",)

    first, *rest = fake.requests
    assert first.HasField("init")
    assert first.init.metadata.user_id == "user-123"
    assert first.init.metadata.audio_encoding == pb.AUDIO_ENCODING_WAV
    assert list(first.init.preferences.language) == [pb.LANGUAGE_ENGLISH_US]
    assert list(first.init.preferences.vocabulary.dictionary_personal) == ["Hermes"]
    assert first.context.app.name == "Test"
    assert first.commit == pb.COMMIT_FALSE
    assert rest[-1].commit == pb.COMMIT_TRUE
    sent = b"".join(p for r in rest for p in r.payload.audio_packets.items)
    assert sent == pcm_1s  # 1 s = exactly 25 packets, no padding

    md = fake.metadata[0]
    assert md["authorization"] == f"Bearer {auth.current().access_token.get_secret_value()}"
    assert md["disable-formatting"] == "false"
    assert "baseten-authorization" not in md  # the app's embedded key is not needed


def test_raw_mode(auth: Authenticator, fake_server: tuple[FakeWispr, str], pcm_1s: bytes) -> None:
    result = TranscriptionClient(auth).transcribe_pcm(pcm_1s, formatting=False)
    assert result.status == "raw_transcript"
    assert result.text == "hello from the fake server"
    assert fake_server[0].metadata[0]["disable-formatting"] == "true"


def test_streaming_partials(auth: Authenticator, pcm_1s: bytes) -> None:
    with TranscriptionClient(auth).open_stream() as session:
        for i in range(0, len(pcm_1s), 1000):  # odd chunk sizes
            session.push_audio(pcm_1s[i : i + 1000])
        result = session.finalize()
    assert result.text == "Hello from the fake server."
    assert session.partial_text == "Hello from the fake server."
    with pytest.raises(TranscriptionError, match="already finalized"):
        session.push_audio(b"\x00\x00")


def test_unauthenticated_forces_refresh_and_retries(
    auth: Authenticator, fake_server: tuple[FakeWispr, str], pcm_1s: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake, _ = fake_server
    fake.reject_tokens.add(auth.current().access_token.get_secret_value())
    fresh = TokenSet.from_tokens(make_jwt(exp_in=9000), "r2")
    monkeypatch.setattr(
        Authenticator, "refresh", lambda self, force=False: (self.store.save(fresh), fresh)[1]
    )

    assert TranscriptionClient(auth).transcribe_pcm(pcm_1s).text == "Hello from the fake server."
    assert len(fake.metadata) == 2


def test_empty_audio_rejected(auth: Authenticator) -> None:
    with pytest.raises(TranscriptionError, match="empty audio"):
        TranscriptionClient(auth).transcribe_pcm(b"")


# --------------------------------------------------------------------------- CLI


@pytest.fixture
def cli_env(auth: Authenticator, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WISPR_HOME", str(auth.settings.home))
    monkeypatch.setenv("WISPR_GRPC_HOST", auth.settings.grpc_host)
    monkeypatch.setenv("WISPR_GRPC_TLS", "false")


@pytest.mark.usefixtures("cli_env")
def test_cli_transcribe_json(tmp_path: Path, pcm_1s: bytes, capsys: pytest.CaptureFixture[str]) -> None:
    audio = tmp_path / "clip.raw"
    audio.write_bytes(pcm_1s)
    assert cli.main(["transcribe", str(audio), "--json", "-l", "en"]) == 0
    event = STREAM_EVENT_ADAPTER.validate_json(capsys.readouterr().out)
    assert isinstance(event, FinalEvent)
    assert event.result.text == "Hello from the fake server."


@pytest.mark.usefixtures("cli_env")
def test_cli_stream(
    pcm_1s: bytes, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    read_fd, write_fd = os.pipe()
    os.write(write_fd, pcm_1s)
    os.close(write_fd)
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(os.fdopen(read_fd, "rb")))
    assert cli.main(["stream"]) == 0
    events = [STREAM_EVENT_ADAPTER.validate_json(line) for line in capsys.readouterr().out.splitlines()]
    assert isinstance(events[-1], FinalEvent)
    assert all(isinstance(e, PartialEvent) for e in events[:-1])


def test_cli_not_logged_in(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("WISPR_HOME", str(tmp_path / "empty"))
    clip = tmp_path / "x.raw"
    clip.write_bytes(b"\x00\x00" * 100)
    assert cli.main(["transcribe", str(clip), "--json"]) == cli.EXIT_AUTH
    assert json.loads(capsys.readouterr().out)["kind"] == "NotLoggedInError"
