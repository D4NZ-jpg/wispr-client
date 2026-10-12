"""``wispr`` command line.

Exit codes: 0 ok, 1 transcription/API failure, 2 usage error, 3 not logged in / auth failure.
``--json`` / ``stream`` emit one :data:`~wispr_client.models.StreamEvent` per line on stdout.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import threading
import webbrowser
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Final

from . import __version__
from .api import WisprApi
from .auth import Authenticator
from .config import WisprSettings
from .errors import AuthError, NotLoggedInError, WisprError
from .models import ErrorEvent, FinalEvent, PartialEvent, StreamEvent
from .transcribe import TranscriptionClient

if TYPE_CHECKING:
    from collections.abc import Sequence

EXIT_OK: Final = 0
EXIT_FAILURE: Final = 1
EXIT_AUTH: Final = 3

Command = Callable[[argparse.Namespace, Authenticator], int]

_STDIN_CHUNK: Final = 3200  # 100 ms of PCM
_PARTIAL_POLL_S: Final = 0.1


def _emit(event: StreamEvent) -> None:
    sys.stdout.write(event.model_dump_json() + "\n")
    sys.stdout.flush()


def _exit_code(exc: WisprError) -> int:
    return EXIT_AUTH if isinstance(exc, NotLoggedInError | AuthError) else EXIT_FAILURE


def _vocabulary(values: Sequence[str] | None) -> list[str]:
    return [w.strip() for v in values or () for w in v.split(",") if w.strip()]


# --------------------------------------------------------------------------- commands


def cmd_login(args: argparse.Namespace, auth: Authenticator) -> int:
    def show(url: str) -> None:
        print(f"Open this URL and sign in to Wispr Flow:\n\n  {url}\n", file=sys.stderr)
        if not args.no_browser:
            webbrowser.open(url)
        print("Waiting for login...", file=sys.stderr)

    tokens = auth.login_device_code(show, timeout_s=args.timeout)
    name = " ".join(filter(None, (tokens.first_name, tokens.last_name))) or tokens.email or tokens.user_id
    print(f"Logged in as {name} ({tokens.provider}). Session saved.", file=sys.stderr)
    return EXIT_OK


def cmd_logout(_: argparse.Namespace, auth: Authenticator) -> int:
    removed = auth.logout()
    print("Logged out." if removed else "Not logged in.", file=sys.stderr)
    return EXIT_OK


def cmd_status(args: argparse.Namespace, auth: Authenticator) -> int:
    tokens = auth.current()
    if args.refresh:
        tokens = auth.refresh(force=True)
    profile = WisprApi(auth).profile()
    left = tokens.expires_at - datetime.now(UTC)
    print(f"user:     {profile.first_name or ''} {profile.last_name or ''} <{profile.email or '?'}>")
    print(f"provider: {tokens.provider}")
    print(f"token:    valid for {left.total_seconds() / 3600:.1f} h (auto-refreshes)")
    print(f"store:    {auth.store.path}")
    return EXIT_OK


def cmd_transcribe(args: argparse.Namespace, auth: Authenticator) -> int:
    client = TranscriptionClient(auth, app_name=args.app_name)
    try:
        result = client.transcribe_file(
            Path(args.file),
            language=args.language,
            formatting=not args.raw,
            vocabulary=_vocabulary(args.vocab),
        )
    except WisprError as exc:
        if args.json:
            _emit(ErrorEvent(error=str(exc), kind=type(exc).__name__))
            return _exit_code(exc)
        raise
    if args.json:
        _emit(FinalEvent(result=result))
    else:
        print(result.text)
    return EXIT_OK


def cmd_stream(args: argparse.Namespace, auth: Authenticator) -> int:
    """Raw 16 kHz mono s16le PCM on stdin -> JSON-lines partial/final events on stdout."""
    client = TranscriptionClient(auth, app_name=args.app_name)
    try:
        session = client.open_stream(
            language=args.language, formatting=not args.raw, vocabulary=_vocabulary(args.vocab)
        )
    except WisprError as exc:
        _emit(ErrorEvent(error=str(exc), kind=type(exc).__name__))
        return _exit_code(exc)

    with session:
        eof = threading.Event()
        feed_error: list[WisprError] = []

        def feed() -> None:
            try:
                stdin = sys.stdin.fileno()
                while chunk := os.read(stdin, _STDIN_CHUNK):  # returns as soon as data arrives
                    session.push_audio(chunk)
            except WisprError as exc:
                feed_error.append(exc)
            finally:
                eof.set()

        threading.Thread(target=feed, name="wispr-stdin", daemon=True).start()
        last = ""
        while not eof.wait(_PARTIAL_POLL_S):
            if (text := session.partial_text) and text != last:
                last = text
                _emit(PartialEvent(text=text))
        try:
            if feed_error:
                raise feed_error[0]
            _emit(FinalEvent(result=session.finalize()))
        except WisprError as exc:
            _emit(ErrorEvent(error=str(exc), kind=type(exc).__name__))
            return _exit_code(exc)
    return EXIT_OK


# --------------------------------------------------------------------------- parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wispr", description="Unofficial Wispr Flow speech-to-text client")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="log to stderr (-vv for debug)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("login", help="sign in through the browser (device code)")
    p.add_argument("--no-browser", action="store_true", help="only print the URL")
    p.add_argument("--timeout", type=float, default=600.0, help="seconds to wait (default 600)")
    p.set_defaults(func=cmd_login)

    p = sub.add_parser("logout", help="delete the stored session")
    p.set_defaults(func=cmd_logout)

    p = sub.add_parser("status", help="show the logged-in account and token validity")
    p.add_argument("--refresh", action="store_true", help="force a token refresh first")
    p.set_defaults(func=cmd_status)

    def add_transcription_opts(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("-l", "--language", help="ISO/BCP-47 hint, e.g. en, en-GB, es (default: auto)")
        sp.add_argument("--raw", action="store_true", help="plain ASR transcript, skip Wispr formatting")
        sp.add_argument(
            "--vocab",
            action="append",
            metavar="WORDS",
            help="comma-separated custom words/names (repeatable)",
        )
        sp.add_argument("--app-name", default="Hermes Agent", help="app name sent as dictation context")

    p = sub.add_parser("transcribe", help="transcribe an audio file (any format ffmpeg reads)")
    p.add_argument("file", help="audio file; .raw/.pcm = 16 kHz mono s16le")
    p.add_argument("--json", action="store_true", help="print a JSON event instead of plain text")
    add_transcription_opts(p)
    p.set_defaults(func=cmd_transcribe)

    p = sub.add_parser("stream", help="live: read 16 kHz mono s16le PCM from stdin, emit JSON lines")
    add_transcription_opts(p)
    p.set_defaults(func=cmd_stream)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    level = {0: logging.WARNING, 1: logging.INFO}.get(args.verbose, logging.DEBUG)
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s", stream=sys.stderr)
    try:
        command: Command = args.func
        code = command(args, Authenticator(WisprSettings()))  # settings read from env once, here
    except KeyboardInterrupt:
        return 130
    except WisprError as exc:
        print(f"wispr: {exc}", file=sys.stderr)
        return _exit_code(exc)
    return code


if __name__ == "__main__":
    sys.exit(main())
