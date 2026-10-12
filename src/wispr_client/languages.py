"""Map ISO-639-1 / BCP-47 language hints (``en``, ``en-GB``, ``pt-BR``) to Wispr's Language enum.

Wispr's enum follows Whisper's language list, so the ISO codes Whisper uses map one-to-one.
Unknown or empty hints map to ``None``: no language is sent and the server auto-detects.
"""

from __future__ import annotations

# base ISO code -> enum suffix (without the LANGUAGE_ prefix)
_ISO: dict[str, str] = {
    "en": "ENGLISH_US",
    "zh": "CHINESE_SIMPLIFIED",
    "de": "GERMAN",
    "es": "SPANISH",
    "ru": "RUSSIAN",
    "ko": "KOREAN",
    "fr": "FRENCH",
    "ja": "JAPANESE",
    "pt": "PORTUGUESE",
    "tr": "TURKISH",
    "pl": "POLISH",
    "ca": "CATALAN",
    "nl": "DUTCH",
    "ar": "ARABIC",
    "sv": "SWEDISH",
    "it": "ITALIAN",
    "id": "INDONESIAN",
    "hi": "HINDI",
    "fi": "FINNISH",
    "vi": "VIETNAMESE",
    "he": "HEBREW",
    "iw": "HEBREW",
    "uk": "UKRAINIAN",
    "el": "GREEK",
    "ms": "MALAY",
    "cs": "CZECH",
    "ro": "ROMANIAN",
    "da": "DANISH",
    "hu": "HUNGARIAN",
    "ta": "TAMIL",
    "no": "NORWEGIAN",
    "nb": "NORWEGIAN",
    "th": "THAI",
    "ur": "URDU",
    "hr": "CROATIAN",
    "bg": "BULGARIAN",
    "lt": "LITHUANIAN",
    "la": "LATIN",
    "mi": "MAORI",
    "ml": "MALAYALAM",
    "cy": "WELSH",
    "sk": "SLOVAK",
    "te": "TELUGU",
    "fa": "PERSIAN",
    "lv": "LATVIAN",
    "bn": "BENGALI",
    "sr": "SERBIAN",
    "az": "AZERBAIJANI",
    "sl": "SLOVENIAN",
    "kn": "KANNADA",
    "et": "ESTONIAN",
    "mk": "MACEDONIAN",
    "br": "BRETON",
    "eu": "BASQUE",
    "is": "ICELANDIC",
    "hy": "ARMENIAN",
    "ne": "NEPALI",
    "mn": "MONGOLIAN",
    "bs": "BOSNIAN",
    "kk": "KAZAKH",
    "sq": "ALBANIAN",
    "sw": "SWAHILI",
    "gl": "GALICIAN",
    "mr": "MARATHI",
    "pa": "PUNJABI",
    "si": "SINHALA",
    "km": "KHMER",
    "sn": "SHONA",
    "yo": "YORUBA",
    "so": "SOMALI",
    "af": "AFRIKAANS",
    "oc": "OCCITAN",
    "ka": "GEORGIAN",
    "be": "BELARUSIAN",
    "tg": "TAJIK",
    "sd": "SINDHI",
    "gu": "GUJARATI",
    "am": "AMHARIC",
    "yi": "YIDDISH",
    "lo": "LAO",
    "uz": "UZBEK",
    "fo": "FAROESE",
    "ht": "HAITIAN_CREOLE",
    "ps": "PASHTO",
    "tk": "TURKMEN",
    "nn": "NYNORSK",
    "mt": "MALTESE",
    "sa": "SANSKRIT",
    "lb": "LUXEMBOURGISH",
    "my": "MYANMAR",
    "bo": "TIBETAN",
    "tl": "TAGALOG",
    "fil": "TAGALOG",
    "mg": "MALAGASY",
    "as": "ASSAMESE",
    "tt": "TATAR",
    "haw": "HAWAIIAN",
    "ln": "LINGALA",
    "ha": "HAUSA",
    "ba": "BASHKIR",
    "jw": "JAVANESE",
    "jv": "JAVANESE",
    "su": "SUNDANESE",
    "yue": "CANTONESE",
    "gsw": "GERMAN_SWISS",
}

# full tag -> enum suffix, checked before the base code
_REGIONAL: dict[str, str] = {
    "en-gb": "ENGLISH_UK",
    "en-uk": "ENGLISH_UK",
    "en-ca": "ENGLISH_CA",
    "en-us": "ENGLISH_US",
    "zh-tw": "CHINESE_TRADITIONAL",
    "zh-hk": "CANTONESE",
    "zh-hant": "CHINESE_TRADITIONAL",
    "zh-hans": "CHINESE_SIMPLIFIED",
    "zh-cn": "CHINESE_SIMPLIFIED",
    "de-ch": "GERMAN_SWISS",
    "hi-latn": "HINGLISH",
}


def to_wispr_language(hint: str | None) -> str | None:
    """Return a ``LANGUAGE_*`` enum name for *hint*, or ``None`` for auto-detect."""
    if not hint:
        return None
    if hint.strip().upper().startswith("LANGUAGE_"):  # already an enum name
        return hint.strip().upper()
    tag = hint.strip().replace("_", "-").lower()
    if not tag or tag in {"auto", "und"}:
        return None
    suffix = _REGIONAL.get(tag) or _ISO.get(tag.split("-")[0])
    return f"LANGUAGE_{suffix}" if suffix else None


def from_wispr_language(enum_name: str) -> str:
    """Best-effort reverse mapping (``LANGUAGE_ENGLISH_UK`` -> ``en-GB``); unknown -> lowercased suffix."""
    suffix = enum_name.removeprefix("LANGUAGE_")
    for code, s in _ISO.items():  # prefer the plain ISO code (en, es, ...)
        if s == suffix:
            return code
    for tag, s in _REGIONAL.items():
        if s == suffix:
            base, _, region = tag.partition("-")
            return f"{base}-{region.upper()}" if len(region) == 2 else tag
    return suffix.lower()
