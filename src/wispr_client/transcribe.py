"""Dictation over gRPC: ``flow_api.v1.TranscriptionService/TranscribeStream``.

Protocol (verified against the live service):

1. first message: ``init`` (metadata, preferences) + ``context``, ``commit=FALSE``
2. audio messages: ``payload.audio_packets`` of 40 ms 16 kHz s16le packets, ``commit=FALSE``
3. ``commit=TRUE``, then half-close the request stream
4. the server streams ``heartbeat`` / partial ``state`` messages and finally one ``result``.
   The final result is only emitted after the client half-closes.

The unary ``Transcribe`` RPC is rejected by the production proxy (UNIMPLEMENTED).
"""

from __future__ import annotations

import logging
import queue
import threading
import uuid
from contextlib import AbstractContextManager
from typing import TYPE_CHECKING, Final, Literal

import grpc

from ._proto import flow_api_v1_pb2 as pb
from .audio import Packetizer, load_pcm
from .auth import Authenticator
from .errors import TranscriptionError
from .languages import from_wispr_language, to_wispr_language
from .models import ResultStatus, TranscriptionResult

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
    from pathlib import Path
    from types import TracebackType
    from typing import TypeAlias

    # Only the grpc-stubs class is generic; the runtime class is not subscriptable.
    _Call: TypeAlias = grpc.StreamStreamMultiCallable[pb.Request, pb.Response]

_log = logging.getLogger(__name__)

_METHOD: Final = "/flow_api.v1.TranscriptionService/TranscribeStream"
_MAX_PACKETS_PER_MESSAGE: Final = 25  # ~1 s of audio, as the desktop app sends
_STATUS: Final[dict[int, ResultStatus]] = {
    pb.RESULT_STATUS_FORMATTED: "formatted",
    pb.RESULT_STATUS_RAW_TRANSCRIPT: "raw_transcript",
    pb.RESULT_STATUS_ERROR: "error",
}

AppType = Literal[
    "APP_TYPE_OTHER",
    "APP_TYPE_BROWSER",
    "APP_TYPE_PERSONAL_MESSAGING",
    "APP_TYPE_WORK_MESSAGING",
    "APP_TYPE_EMAIL",
    "APP_TYPE_CHATBOT",
    "APP_TYPE_DEVELOPER",
]

_channels: dict[str, grpc.Channel] = {}
_channels_lock = threading.Lock()


_CHANNEL_OPTIONS: Final = [("grpc.keepalive_time_ms", 30_000), ("grpc.keepalive_permit_without_calls", 1)]


def _channel(host: str, *, tls: bool = True) -> grpc.Channel:
    """One shared channel per host: keeps the HTTP/2 connection warm between dictations."""
    with _channels_lock:
        if (channel := _channels.get(host)) is None:
            channel = (
                grpc.secure_channel(host, grpc.ssl_channel_credentials(), options=_CHANNEL_OPTIONS)
                if tls
                else grpc.insecure_channel(host, options=_CHANNEL_OPTIONS)
            )
            _channels[host] = channel
        return channel


class StreamSession(AbstractContextManager["StreamSession"]):
    """One utterance. ``push_audio`` is thread-safe; ``finalize`` blocks for the final result.

    Use as a context manager so an abandoned session is cancelled::

        with client.open_stream(language="en") as session:
            for chunk in mic:
                session.push_audio(chunk)
            result = session.finalize()
    """

    def __init__(
        self,
        call_factory: _Call,
        metadata: Sequence[tuple[str, str]],
        first: pb.Request,
        request_id: str,
        timeout_s: float,
    ) -> None:
        self.request_id = request_id
        # ``None`` is the half-close sentinel for the request iterator.
        self._requests: queue.SimpleQueue[pb.Request | None] = queue.SimpleQueue()
        self._requests.put(first)
        self._packetizer = Packetizer()
        self._push_lock = threading.Lock()
        self._closed = False
        self._partial = ""
        self._raw_partial = ""
        self._result: pb.Result | None = None
        self._error: TranscriptionError | None = None
        self._done = threading.Event()
        self._call = call_factory(self._iter_requests(), metadata=tuple(metadata), timeout=timeout_s)
        self._reader = threading.Thread(target=self._read, name=f"wispr-stream-{request_id[:8]}", daemon=True)
        self._reader.start()

    # ------------------------------------------------------------------ producer side

    def push_audio(self, chunk: bytes) -> None:
        """Feed 16 kHz mono s16le PCM of any size."""
        if not chunk:
            return
        with self._push_lock:
            if self._closed:
                raise TranscriptionError("session already finalized")
            self._send_packets(self._packetizer.feed(chunk))

    @property
    def partial_text(self) -> str:
        """Latest interim text (formatted when available, else raw ASR)."""
        return self._partial or self._raw_partial

    def finalize(self, timeout_s: float = 60.0) -> TranscriptionResult:
        """Flush, commit, half-close and wait for the server's final result."""
        with self._push_lock:
            if not self._closed:
                self._send_packets(self._packetizer.flush())
                self._requests.put(pb.Request(commit=pb.COMMIT_TRUE))
                self._requests.put(None)
                self._closed = True
        if not self._done.wait(timeout_s):
            self.cancel()
            raise TranscriptionError(f"no final result within {timeout_s:.0f}s", code="DEADLINE_EXCEEDED")
        if self._error is not None:
            raise self._error
        if self._result is None:
            raise TranscriptionError("stream ended without a result", code="NO_RESULT")
        return self._to_result(self._result)

    def cancel(self) -> None:
        with self._push_lock:
            if not self._closed:
                self._requests.put(None)
                self._closed = True
        self._call.cancel()  # type: ignore[no-untyped-call]  # untyped in grpc-stubs

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        if not self._done.is_set():
            self.cancel()

    def _send_packets(self, packets: list[bytes]) -> None:
        for i in range(0, len(packets), _MAX_PACKETS_PER_MESSAGE):
            batch = packets[i : i + _MAX_PACKETS_PER_MESSAGE]
            self._requests.put(
                pb.Request(
                    payload=pb.Payload(audio_packets=pb.AudioPackets(items=batch)), commit=pb.COMMIT_FALSE
                )
            )

    def _iter_requests(self) -> Iterator[pb.Request]:
        while (item := self._requests.get()) is not None:
            yield item

    # ------------------------------------------------------------------ consumer side

    def _read(self) -> None:
        try:
            for response in self._call:
                if response.HasField("state"):
                    self._update_partial(response.state)
                for state in response.all_states:
                    self._update_partial(state)
                if response.HasField("result"):
                    self._result = response.result
        except grpc.RpcError as exc:
            if exc.code() != grpc.StatusCode.CANCELLED or self._result is None:
                self._error = TranscriptionError(
                    f"Wispr stream failed: {exc.details()}", code=exc.code().name
                )
        finally:
            self._done.set()

    def _update_partial(self, state: pb.State) -> None:
        if state.formatted_text.content:
            self._partial = state.formatted_text.content
        if state.raw_text.content:
            self._raw_partial = state.raw_text.content

    def _to_result(self, result: pb.Result) -> TranscriptionResult:
        status = _STATUS.get(result.status, "unspecified")
        if status == "error":
            raise TranscriptionError("Wispr returned an error result", code="RESULT_ERROR")
        out = result.output
        duration = result.audio_duration.seconds + result.audio_duration.nanos / 1e9
        return TranscriptionResult(
            text=(out.plaintext or self._partial or self._raw_partial).strip(),
            raw_text=self._raw_partial.strip(),
            languages=tuple(from_wispr_language(pb.Language.Name(lang)) for lang in out.languages),
            status=status,
            confidence=out.confidence if out.confidence else None,
            audio_seconds=duration or None,
            origin=result.transcript_origin or None,
            request_id=self.request_id,
        )


class TranscriptionClient:
    """High-level entry point.

    ``formatting=False`` returns Wispr's raw ASR transcript (no LLM clean-up).
    ``vocabulary`` adds custom words/names to the request's personal dictionary.
    """

    def __init__(
        self,
        auth: Authenticator | None = None,
        *,
        app_name: str = "Hermes Agent",
        app_type: AppType = "APP_TYPE_OTHER",
    ) -> None:
        self.auth = auth or Authenticator()
        self.settings = self.auth.settings
        self.app_name = app_name
        self.app_type = app_type
        self._session_id = str(uuid.uuid4())

    def open_stream(
        self, *, language: str | None = None, formatting: bool = True, vocabulary: Sequence[str] = ()
    ) -> StreamSession:
        token = self.auth.access_token()
        tokens = self.auth.current()
        request_id = str(uuid.uuid4())
        factory = _channel(self.settings.grpc_host, tls=self.settings.grpc_tls).stream_stream(
            _METHOD,
            request_serializer=pb.Request.SerializeToString,
            response_deserializer=pb.Response.FromString,
        )
        return StreamSession(
            factory,
            self._metadata(token, formatting=formatting),
            self._first_request(tokens.user_id, request_id, language, vocabulary),
            request_id,
            self.settings.stream_timeout_s,
        )

    def transcribe_pcm(
        self,
        pcm: bytes,
        *,
        language: str | None = None,
        formatting: bool = True,
        vocabulary: Sequence[str] = (),
    ) -> TranscriptionResult:
        """Transcribe a complete recording; retries once after a forced token refresh on UNAUTHENTICATED."""
        if not pcm:
            raise TranscriptionError("empty audio", code="EMPTY_AUDIO")
        for attempt in range(2):
            with self.open_stream(language=language, formatting=formatting, vocabulary=vocabulary) as s:
                s.push_audio(pcm)
                try:
                    return s.finalize()
                except TranscriptionError as exc:
                    if exc.code != "UNAUTHENTICATED" or attempt:
                        raise
                    _log.info("access token rejected; forcing refresh and retrying")
                    self.auth.refresh(force=True)
        raise AssertionError("unreachable")  # pragma: no cover

    def transcribe_file(
        self,
        path: Path,
        *,
        language: str | None = None,
        formatting: bool = True,
        vocabulary: Sequence[str] = (),
    ) -> TranscriptionResult:
        return self.transcribe_pcm(
            load_pcm(path), language=language, formatting=formatting, vocabulary=vocabulary
        )

    # ------------------------------------------------------------------ request building

    def _metadata(self, token: str, *, formatting: bool) -> list[tuple[str, str]]:
        return [
            ("authorization", f"Bearer {token}"),
            ("baseten-model-id", f"model-{self.settings.model_id}"),
            ("x-baseten-environment", "production"),
            ("flow-debug", "false"),
            ("disable-formatting", "false" if formatting else "true"),
        ]

    def _first_request(
        self, user_id: str, request_id: str, language: str | None, vocabulary: Sequence[str]
    ) -> pb.Request:
        major, minor, patch = self.settings.version_tuple
        lang = to_wispr_language(language)
        prefs = pb.Preferences(
            language=[lang] if lang else [],  # enum names are accepted by the constructor
            vocabulary=pb.StaticVocabulary(dictionary_personal=[v for v in vocabulary if v.strip()]),
        )
        return pb.Request(
            init=pb.Init(
                metadata=pb.Metadata(
                    user_id=user_id,
                    session_id=self._session_id,
                    request_id=request_id,
                    audio_encoding=pb.AUDIO_ENCODING_WAV,
                    environment=pb.ENVIRONMENT_PRODUCTION,
                    client=pb.Client(
                        name=self.settings.client_name,
                        platform=self.settings.platform,
                        version=pb.Version(major=major, minor=minor, patch=patch),
                    ),
                ),
                preferences=prefs,
            ),
            context=pb.Context(app=pb.App(name=self.app_name, type=self.app_type)),
            commit=pb.COMMIT_FALSE,
        )
