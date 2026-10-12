"""Audio input: everything is normalised to 16 kHz mono signed 16-bit little-endian PCM."""

from __future__ import annotations

import shutil
import subprocess
import wave
from typing import TYPE_CHECKING, Final

from .errors import AudioError

if TYPE_CHECKING:
    from pathlib import Path

SAMPLE_RATE: Final = 16_000
SAMPLE_WIDTH: Final = 2  # bytes, s16le
BYTES_PER_SECOND: Final = SAMPLE_RATE * SAMPLE_WIDTH
PACKET_MS: Final = 40  # Wispr Flow's WAV packet size
PACKET_BYTES: Final = BYTES_PER_SECOND * PACKET_MS // 1000  # 1280

RAW_SUFFIXES: Final = frozenset({".raw", ".pcm", ".s16le"})


def ffmpeg_path() -> str | None:
    return shutil.which("ffmpeg")


def load_pcm(path: Path, *, timeout_s: float = 120.0) -> bytes:
    """Decode any audio file to 16 kHz mono s16le.

    ``.raw``/``.pcm`` files are assumed to already be in that format. Matching WAV files are read
    with the standard library; everything else needs ``ffmpeg`` on ``PATH``.
    """
    if not path.is_file():
        raise AudioError(f"no such audio file: {path}")
    if path.suffix.lower() in RAW_SUFFIXES:
        return _even(path.read_bytes())
    if path.suffix.lower() == ".wav" and (pcm := _read_native_wav(path)) is not None:
        return pcm
    return _ffmpeg_decode(path, timeout_s)


def _read_native_wav(path: Path) -> bytes | None:
    """PCM from a WAV already at 16 kHz/mono/16-bit, else ``None`` (needs resampling)."""
    try:
        with wave.open(str(path), "rb") as wav:
            if (wav.getframerate(), wav.getnchannels(), wav.getsampwidth()) != (SAMPLE_RATE, 1, SAMPLE_WIDTH):
                return None
            return wav.readframes(wav.getnframes())
    except (wave.Error, EOFError):
        return None


def _ffmpeg_decode(path: Path, timeout_s: float) -> bytes:
    exe = ffmpeg_path()
    if exe is None:
        raise AudioError(f"ffmpeg is required to decode {path.suffix or 'this'} audio; install ffmpeg")
    cmd = [
        exe,
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        str(SAMPLE_RATE),
        "-f",
        "s16le",
        "-acodec",
        "pcm_s16le",
        "pipe:1",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout_s, check=False)
    except subprocess.TimeoutExpired as exc:
        raise AudioError(f"ffmpeg timed out decoding {path}") from exc
    if proc.returncode != 0:
        raise AudioError(
            f"ffmpeg could not decode {path}: {proc.stderr.decode(errors='replace').strip()[:300]}"
        )
    if not proc.stdout:
        raise AudioError(f"{path} contains no audio")
    return _even(proc.stdout)


def _even(pcm: bytes) -> bytes:
    return pcm[: len(pcm) - (len(pcm) % SAMPLE_WIDTH)]


def duration_seconds(pcm: bytes) -> float:
    return len(pcm) / BYTES_PER_SECOND


class Packetizer:
    """Accumulates arbitrary PCM chunks and yields whole 40 ms packets."""

    __slots__ = ("_buf",)

    def __init__(self) -> None:
        self._buf = bytearray()

    def feed(self, chunk: bytes) -> list[bytes]:
        self._buf += chunk
        whole = len(self._buf) - len(self._buf) % PACKET_BYTES
        packets = [bytes(self._buf[i : i + PACKET_BYTES]) for i in range(0, whole, PACKET_BYTES)]
        del self._buf[:whole]
        return packets

    def flush(self) -> list[bytes]:
        """Remaining audio, zero-padded to one full packet."""
        if not self._buf:
            return []
        packet = bytes(self._buf).ljust(PACKET_BYTES, b"\x00")
        self._buf.clear()
        return [packet]
