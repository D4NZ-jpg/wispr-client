# wispr-client

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](pyproject.toml)
[![Typed](https://img.shields.io/badge/typing-mypy%20strict-informational)](pyproject.toml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230)](https://github.com/astral-sh/ruff)

Unofficial, typed Python client and CLI for [Wispr Flow](https://wisprflow.ai) speech-to-text. It uses your own Wispr account.

> [!NOTE]
> Last verified working with Wispr Flow **1.6.1102**. Later app versions can change the API.

[Features](#features) • [Installation](#installation) • [CLI usage](#cli-usage) • [Library usage](#library-usage) • [Configuration](#configuration) • [How it works](#how-it-works) • [Development](#development)

> [!WARNING]
> This project is not affiliated with or endorsed by Wispr. The API is undocumented and can change without notice. Automated use may violate Wispr's terms of service. Every transcription counts against your Wispr plan.

## Features

- **Browser login** with the same device-code flow as the desktop app. The session is stored locally and refreshed automatically.
- **File transcription** for any audio format that ffmpeg can decode.
- **Live streaming** from raw PCM on stdin, with JSON-lines output.
- **Wispr formatting or raw ASR**: use Wispr's cleaned-up text, or turn it off with `--raw`.
- **Custom vocabulary** for names and uncommon words.
- **Language hints** with ISO-639-1 / BCP-47 codes (`en`, `en-GB`, `pt-BR`). If you omit the hint, the server detects the language.
- **Typed library API**: pydantic v2 models, a `py.typed` marker, and code that passes `mypy --strict`.

## Installation

You need Python 3.11 or later and [uv](https://docs.astral.sh/uv/).

```bash
uv tool install git+https://github.com/D4NZ-jpg/wispr-client
```

This puts the `wispr` command on your `PATH`.

> [!NOTE]
> To decode anything other than 16 kHz mono WAV or raw PCM (`.raw`, `.pcm`, `.s16le`), install [ffmpeg](https://ffmpeg.org) and put it on your `PATH`.

To use the library in another project:

```bash
uv add git+https://github.com/D4NZ-jpg/wispr-client
```

## CLI usage

Sign in once. This opens `wisprflow.ai` in your browser and saves the session:

```bash
wispr login                # add --no-browser to only print the URL
wispr status               # account, token validity, and token file path
wispr logout               # delete the stored session
```

Transcribe a file:

```bash
wispr transcribe note.ogg -l en             # plain text on stdout
wispr transcribe note.ogg --raw             # raw ASR, no Wispr formatting
wispr transcribe note.ogg --vocab "Hermes,Nous" --vocab Kubernetes
wispr transcribe note.ogg --json            # one JSON event, see below
```

Stream live audio as 16 kHz mono signed 16-bit little-endian PCM on stdin:

```bash
# Linux (ALSA)
arecord -f S16_LE -r 16000 -c 1 -t raw | wispr stream -l en

# macOS / any platform with ffmpeg
ffmpeg -f avfoundation -i ":0" -ac 1 -ar 16000 -f s16le - | wispr stream -l en
```

Options shared by `transcribe` and `stream`:

| Option | Description |
|---|---|
| `-l`, `--language` | Language hint, for example `en`, `en-GB`, `es`. Default: auto-detect. |
| `--raw` | Return the plain ASR transcript without Wispr formatting. |
| `--vocab WORDS` | Comma-separated custom words or names. You can repeat this option. |
| `--app-name` | App name sent as dictation context. Default: `Hermes Agent`. |

Use `-v` for info logs or `-vv` for debug logs on stderr.

| Exit code | Meaning |
|---|---|
| `0` | Success |
| `1` | Transcription or API failure |
| `2` | Usage error |
| `3` | Not logged in, or authentication failed |
| `130` | Interrupted |

### JSON event contract

`transcribe --json` and `stream` write one JSON object per line to stdout. You can validate each line with `wispr_client.STREAM_EVENT_ADAPTER`:

```json
{"v":1,"type":"partial","text":"..."}
{"v":1,"type":"final","result":{"text":"...","raw_text":"...","languages":["en"],"status":"formatted","confidence":1.0,"audio_seconds":11.0,"origin":"canto_1.0.1","request_id":"..."}}
{"v":1,"type":"error","error":"...","kind":"AuthError"}
```

> [!TIP]
> Wispr returns text only after the utterance is committed. In practice, `stream` emits the `final` event about 0.4 s after the audio ends, with few or no `partial` events before it.

## Library usage

`TranscriptionClient` uses the session that `wispr login` saved.

```python
from pathlib import Path
from wispr_client import TranscriptionClient

client = TranscriptionClient()
result = client.transcribe_file(Path("note.ogg"), language="en", vocabulary=["Hermes", "Nous"])
print(result.text, result.languages, result.status)
```

For live audio, open a stream session. You can call `push_audio` from any thread, with chunks of any size:

```python
with client.open_stream(language="en", formatting=True) as session:
    for chunk in mic_chunks():  # 16 kHz mono s16le
        session.push_audio(chunk)
    print(session.finalize().text)
```

If you already have PCM bytes, use `client.transcribe_pcm(pcm, ...)`. If the server rejects the access token, `transcribe_pcm` and `transcribe_file` refresh the token and retry once.

Public data types are pydantic v2 models: `TokenSet`, `TranscriptionResult`, `UserProfile`, and the stream events `PartialEvent`, `FinalEvent`, and `ErrorEvent`. All errors derive from `WisprError`:

| Error | Raised when |
|---|---|
| `NotLoggedInError` | No stored session exists. |
| `AuthError` | Login or token refresh fails. |
| `AudioError` | The audio file cannot be read or decoded. |
| `TranscriptionError` | The dictation stream fails. Has a `.code` attribute. |
| `ApiError` | A REST call fails. Has a `.status` attribute. |

## Configuration

All settings are in [`config.py`](src/wispr_client/config.py). You can override each one with an environment variable that has the `WISPR_` prefix. The most useful ones:

| Variable | Default | Description |
|---|---|---|
| `WISPR_HOME` | `$XDG_CONFIG_HOME/wispr-client` or `~/.config/wispr-client` | Directory for `tokens.json` (file mode `0600`). |
| `WISPR_STREAM_TIMEOUT_S` | `600` | Maximum duration of one dictation stream, in seconds. |
| `WISPR_HTTP_TIMEOUT_S` | `15` | Timeout for REST calls, in seconds. |
| `WISPR_REFRESH_SKEW_S` | `300` | Refresh the token this many seconds before it expires. |
| `WISPR_GRPC_HOST` | `inference.wisprflow.com:443` | gRPC transcription endpoint. |
| `WISPR_API_BASE` | `https://api.wisprflow.ai` | REST API base URL. |
| `WISPR_CLIENT_VERSION` | `1.6.1102` | Desktop app version that the client reports to the server. |
| `WISPR_PLATFORM` | `PLATFORM_WIN32` | Reported platform: `PLATFORM_WIN32` or `PLATFORM_MACOS`. |

## How it works

| Part | Details |
|---|---|
| Login | Device code: open `wisprflow.ai/login?device_code=<uuid>`, then poll `api.wisprflow.ai/device/poll`. |
| Session | Supabase JWT, valid for about 7 days. The client refreshes it through `supabase.co/auth/v1/token`. Refresh tokens are single-use, so the client rotates them under a cross-process file lock. |
| Dictation | gRPC `flow_api.v1.TranscriptionService/TranscribeStream` on `inference.wisprflow.com:443` with `authorization: Bearer <token>`. Sequence: init and context, then 40 ms PCM packets, then `COMMIT_TRUE`, then half-close, then the result. |
| REST | `api.wisprflow.ai` with `Authorization: <token>` (no `Bearer` prefix). |

The protobuf schema is in [`proto/flow_api_v1.proto`](proto/flow_api_v1.proto). To regenerate the Python module after you change it, run `scripts/gen_proto.sh`.

## Development

```bash
uv sync
uv run pytest            # offline tests against an in-process fake gRPC server
uv run pytest -m live    # tests against the real service; run `wispr login` first
uv run ruff check . && uv run ruff format --check . && uv run mypy src tests
```

> [!CAUTION]
> Live tests send real audio to Wispr and use your plan's quota.
