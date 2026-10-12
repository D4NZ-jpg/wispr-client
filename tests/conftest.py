from __future__ import annotations

import base64
import json
import threading
import time
from collections.abc import Iterator
from concurrent import futures
from dataclasses import dataclass, field
from pathlib import Path

import grpc
import pytest

from wispr_client._proto import flow_api_v1_pb2 as pb
from wispr_client.auth import Authenticator, TokenStore
from wispr_client.config import WisprSettings
from wispr_client.models import TokenSet


def make_jwt(sub: str = "user-123", *, exp_in: int = 3600, iss: str = "https://x.supabase.co/auth/v1") -> str:
    def enc(obj: dict[str, object]) -> str:
        return base64.urlsafe_b64encode(json.dumps(obj).encode()).rstrip(b"=").decode()

    claims = {"sub": sub, "exp": int(time.time()) + exp_in, "iss": iss, "email": "dan@example.com"}
    return f"{enc({'alg': 'none'})}.{enc(claims)}.sig"


@dataclass
class FakeWispr:
    """In-process stand-in for inference.wisprflow.com implementing TranscribeStream."""

    text: str = "Hello from the fake server."
    reject_tokens: set[str] = field(default_factory=set)
    requests: list[pb.Request] = field(default_factory=list)
    metadata: list[dict[str, str]] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def handle(
        self, request_iterator: Iterator[pb.Request], context: grpc.ServicerContext
    ) -> Iterator[pb.Response]:
        md = {k: v for k, v in context.invocation_metadata() if isinstance(v, str)}
        with self.lock:
            self.metadata.append(md)
        if md.get("authorization", "").removeprefix("Bearer ") in self.reject_tokens:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "bad token")
        audio_bytes = 0
        committed = False
        for req in request_iterator:  # ends when the client half-closes
            with self.lock:
                self.requests.append(req)
            audio_bytes += sum(len(p) for p in req.payload.audio_packets.items)
            committed = committed or req.commit == pb.COMMIT_TRUE
            yield pb.Response(
                heartbeat=pb.Heartbeat(audio_received_seconds=audio_bytes / 32000, commit_ack=committed)
            )
            yield pb.Response(state=pb.State(raw_text=pb.Text(content=self.text.lower().rstrip("."))))
        if not committed:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, "no commit")
        disable = md.get("disable-formatting") == "true"
        state = pb.State(
            raw_text=pb.Text(content=self.text.lower().rstrip(".")),
            formatted_text=pb.Text(content="" if disable else self.text),
        )
        yield pb.Response(state=state)
        yield pb.Response(
            result=pb.Result(
                output=pb.Transcription(
                    plaintext=self.text.lower().rstrip(".") if disable else self.text,
                    languages=[pb.LANGUAGE_ENGLISH_US],
                    confidence=0.9,
                ),
                status=pb.RESULT_STATUS_RAW_TRANSCRIPT if disable else pb.RESULT_STATUS_FORMATTED,
                transcript_origin="fake",
            )
        )


@pytest.fixture
def fake_server() -> Iterator[tuple[FakeWispr, str]]:
    fake = FakeWispr()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    handler = grpc.stream_stream_rpc_method_handler(
        fake.handle,
        request_deserializer=pb.Request.FromString,
        response_serializer=pb.Response.SerializeToString,
    )
    server.add_generic_rpc_handlers(
        (
            grpc.method_handlers_generic_handler(
                "flow_api.v1.TranscriptionService", {"TranscribeStream": handler}
            ),
        )
    )
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()
    yield fake, f"127.0.0.1:{port}"
    server.stop(grace=None)


@pytest.fixture
def settings(tmp_path: Path, fake_server: tuple[FakeWispr, str]) -> WisprSettings:
    return WisprSettings(home=tmp_path, grpc_host=fake_server[1], grpc_tls=False)


@pytest.fixture
def auth(settings: WisprSettings) -> Authenticator:
    store = TokenStore(settings.token_file)
    store.save(TokenSet.from_tokens(make_jwt(), "refresh-1", first_name="Dan"))
    return Authenticator(settings, store)


@pytest.fixture
def pcm_1s() -> bytes:
    """One second of a quiet 16 kHz s16le signal."""
    return (b"\x10\x00\xf0\xff" * 8000)[:32000]
