# wispr-client

Unofficial, typed Python client and CLI for [Wispr Flow](https://wisprflow.ai) speech-to-text, using
your own Wispr account. Reverse-engineered from the Wispr Flow 1.6.1102 desktop app.

> **Unofficial.** Not affiliated with or endorsed by Wispr. The API is undocumented and can change
> without notice, and automated use may violate Wispr's terms. Dictations count against your plan.

## Install

```bash
uv tool install git+ssh://git@github.com/D4NZ-jpg/wispr-client.git   # puts `wispr` on PATH
```

Decoding anything other than 16 kHz mono WAV / raw PCM needs **ffmpeg** on `PATH`.

## Use

```bash
wispr login                       # opens wisprflow.ai in a browser; session saved and auto-refreshed
wispr status                      # account + token validity
wispr transcribe note.ogg -l en   # any format ffmpeg reads
wispr transcribe note.ogg --raw   # plain ASR, no Wispr formatting/clean-up
wispr transcribe note.ogg --json  # one JSON event (see below)
arecord -f S16_LE -r 16000 -c 1 -t raw | wispr stream -l en   # live: PCM on stdin, JSON lines out
```

Exit codes: `0` ok, `1` transcription/API failure, `2` usage, `3` not logged in / auth failure.

### Library

```python
from pathlib import Path
from wispr_client import TranscriptionClient

client = TranscriptionClient()  # uses the `wispr login` session
result = client.transcribe_file(Path("note.ogg"), language="en", vocabulary=["Hermes", "Nous"])
print(result.text, result.languages, result.status)

with client.open_stream(language="en") as session:  # live, thread-safe push_audio
    for chunk in mic_chunks():  # 16 kHz mono s16le, any size
        session.push_audio(chunk)
    print(session.finalize().text)
```

All public data is pydantic v2 (`TokenSet`, `TranscriptionResult`, `UserProfile`), errors derive from
`WisprError` (`NotLoggedInError`, `AuthError`, `AudioError`, `TranscriptionError`, `ApiError`).

### JSON event contract (`--json`, `stream`)

One object per line, validated by `wispr_client.STREAM_EVENT_ADAPTER`:

```json
{"v":1,"type":"partial","text":"..."}
{"v":1,"type":"final","result":{"text":"...","raw_text":"...","languages":["en"],"status":"formatted","confidence":1.0,"audio_seconds":11.0,"origin":"canto_1.0.1","request_id":"..."}}
{"v":1,"type":"error","error":"...","kind":"AuthError"}
```

Wispr only returns text after the utterance is committed, so in practice `stream` emits the final event
(about 0.4 s after the audio ends) and few or no partials.

## Configuration

Environment variables (`WISPR_` prefix, see `config.py`): `WISPR_HOME` (default `~/.config/wispr-client`,
holds `tokens.json` with mode 0600), `WISPR_GRPC_HOST`, `WISPR_API_BASE`, `WISPR_STREAM_TIMEOUT_S`, ...

## How it works

| | |
|---|---|
| Login | Device code: `wisprflow.ai/login?device_code=<uuid>`, then poll `api.wisprflow.ai/device/poll` |
| Session | Supabase JWT (≈7 days), refreshed via `supabase.co/auth/v1/token`; single-use refresh tokens are rotated under a cross-process file lock |
| Dictation | gRPC `flow_api.v1.TranscriptionService/TranscribeStream` on `inference.wisprflow.com:443`, `authorization: Bearer <token>`; init+context → 40 ms PCM packets → `COMMIT_TRUE` → half-close → result |
| REST | `api.wisprflow.ai`, `Authorization: <token>` (no `Bearer`) |

The schema is in `proto/flow_api_v1.proto` (reconstructed from the app); regenerate the Python module with
`scripts/gen_proto.sh`.

## Development

```bash
uv sync
uv run pytest            # offline: fake in-process gRPC server
uv run pytest -m live    # real service, needs `wispr login`
uv run ruff check . && uv run ruff format --check . && uv run mypy src tests
```
