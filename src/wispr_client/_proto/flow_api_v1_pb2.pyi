import datetime

from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Platform(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PLATFORM_UNSPECIFIED: _ClassVar[Platform]
    PLATFORM_MACOS: _ClassVar[Platform]
    PLATFORM_WIN32: _ClassVar[Platform]
    PLATFORM_IOS: _ClassVar[Platform]
    PLATFORM_ANDROID: _ClassVar[Platform]
    PLATFORM_WEB: _ClassVar[Platform]
    PLATFORM_API: _ClassVar[Platform]

class AppType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    APP_TYPE_UNSPECIFIED: _ClassVar[AppType]
    APP_TYPE_OTHER: _ClassVar[AppType]
    APP_TYPE_BROWSER: _ClassVar[AppType]
    APP_TYPE_PERSONAL_MESSAGING: _ClassVar[AppType]
    APP_TYPE_WORK_MESSAGING: _ClassVar[AppType]
    APP_TYPE_EMAIL: _ClassVar[AppType]
    APP_TYPE_CHATBOT: _ClassVar[AppType]
    APP_TYPE_DEVELOPER: _ClassVar[AppType]

class ChatRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHAT_ROLE_UNSPECIFIED: _ClassVar[ChatRole]
    CHAT_ROLE_USER: _ClassVar[ChatRole]
    CHAT_ROLE_HUMAN: _ClassVar[ChatRole]
    CHAT_ROLE_ASSISTANT: _ClassVar[ChatRole]

class AudioEncoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUDIO_ENCODING_UNSPECIFIED: _ClassVar[AudioEncoding]
    AUDIO_ENCODING_WAV: _ClassVar[AudioEncoding]
    AUDIO_ENCODING_OPUS: _ClassVar[AudioEncoding]

class Environment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENVIRONMENT_UNSPECIFIED: _ClassVar[Environment]
    ENVIRONMENT_PRODUCTION: _ClassVar[Environment]
    ENVIRONMENT_STAGING: _ClassVar[Environment]
    ENVIRONMENT_DEVELOPMENT: _ClassVar[Environment]
    ENVIRONMENT_TEST: _ClassVar[Environment]

class WritingStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WRITING_STYLE_UNSPECIFIED: _ClassVar[WritingStyle]
    WRITING_STYLE_FORMAL: _ClassVar[WritingStyle]
    WRITING_STYLE_CASUAL: _ClassVar[WritingStyle]
    WRITING_STYLE_VERY_CASUAL: _ClassVar[WritingStyle]
    WRITING_STYLE_EXCITED: _ClassVar[WritingStyle]
    WRITING_STYLE_GENZ: _ClassVar[WritingStyle]

class FlowSignaturePrefix(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FLOW_SIGNATURE_PREFIX_UNSPECIFIED: _ClassVar[FlowSignaturePrefix]
    FLOW_SIGNATURE_PREFIX_SPOKEN: _ClassVar[FlowSignaturePrefix]
    FLOW_SIGNATURE_PREFIX_WRITTEN: _ClassVar[FlowSignaturePrefix]

class EditingStrength(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EDITING_STRENGTH_UNSPECIFIED: _ClassVar[EditingStrength]
    EDITING_STRENGTH_VERBATIM: _ClassVar[EditingStrength]
    EDITING_STRENGTH_LIGHT: _ClassVar[EditingStrength]
    EDITING_STRENGTH_MEDIUM: _ClassVar[EditingStrength]
    EDITING_STRENGTH_HEAVY: _ClassVar[EditingStrength]

class Language(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LANGUAGE_UNSPECIFIED: _ClassVar[Language]
    LANGUAGE_ENGLISH_US: _ClassVar[Language]
    LANGUAGE_ENGLISH_UK: _ClassVar[Language]
    LANGUAGE_CHINESE_SIMPLIFIED: _ClassVar[Language]
    LANGUAGE_CHINESE_TRADITIONAL: _ClassVar[Language]
    LANGUAGE_GERMAN: _ClassVar[Language]
    LANGUAGE_SPANISH: _ClassVar[Language]
    LANGUAGE_RUSSIAN: _ClassVar[Language]
    LANGUAGE_KOREAN: _ClassVar[Language]
    LANGUAGE_FRENCH: _ClassVar[Language]
    LANGUAGE_JAPANESE: _ClassVar[Language]
    LANGUAGE_PORTUGUESE: _ClassVar[Language]
    LANGUAGE_TURKISH: _ClassVar[Language]
    LANGUAGE_POLISH: _ClassVar[Language]
    LANGUAGE_CATALAN: _ClassVar[Language]
    LANGUAGE_DUTCH: _ClassVar[Language]
    LANGUAGE_ARABIC: _ClassVar[Language]
    LANGUAGE_SWEDISH: _ClassVar[Language]
    LANGUAGE_ITALIAN: _ClassVar[Language]
    LANGUAGE_INDONESIAN: _ClassVar[Language]
    LANGUAGE_HINDI: _ClassVar[Language]
    LANGUAGE_HINGLISH: _ClassVar[Language]
    LANGUAGE_FINNISH: _ClassVar[Language]
    LANGUAGE_VIETNAMESE: _ClassVar[Language]
    LANGUAGE_HEBREW: _ClassVar[Language]
    LANGUAGE_UKRAINIAN: _ClassVar[Language]
    LANGUAGE_GREEK: _ClassVar[Language]
    LANGUAGE_MALAY: _ClassVar[Language]
    LANGUAGE_CZECH: _ClassVar[Language]
    LANGUAGE_ROMANIAN: _ClassVar[Language]
    LANGUAGE_DANISH: _ClassVar[Language]
    LANGUAGE_HUNGARIAN: _ClassVar[Language]
    LANGUAGE_TAMIL: _ClassVar[Language]
    LANGUAGE_NORWEGIAN: _ClassVar[Language]
    LANGUAGE_THAI: _ClassVar[Language]
    LANGUAGE_URDU: _ClassVar[Language]
    LANGUAGE_CROATIAN: _ClassVar[Language]
    LANGUAGE_BULGARIAN: _ClassVar[Language]
    LANGUAGE_LITHUANIAN: _ClassVar[Language]
    LANGUAGE_LATIN: _ClassVar[Language]
    LANGUAGE_MAORI: _ClassVar[Language]
    LANGUAGE_MALAYALAM: _ClassVar[Language]
    LANGUAGE_WELSH: _ClassVar[Language]
    LANGUAGE_SLOVAK: _ClassVar[Language]
    LANGUAGE_TELUGU: _ClassVar[Language]
    LANGUAGE_PERSIAN: _ClassVar[Language]
    LANGUAGE_LATVIAN: _ClassVar[Language]
    LANGUAGE_BENGALI: _ClassVar[Language]
    LANGUAGE_SERBIAN: _ClassVar[Language]
    LANGUAGE_AZERBAIJANI: _ClassVar[Language]
    LANGUAGE_SLOVENIAN: _ClassVar[Language]
    LANGUAGE_KANNADA: _ClassVar[Language]
    LANGUAGE_ESTONIAN: _ClassVar[Language]
    LANGUAGE_MACEDONIAN: _ClassVar[Language]
    LANGUAGE_BRETON: _ClassVar[Language]
    LANGUAGE_BASQUE: _ClassVar[Language]
    LANGUAGE_ICELANDIC: _ClassVar[Language]
    LANGUAGE_ARMENIAN: _ClassVar[Language]
    LANGUAGE_NEPALI: _ClassVar[Language]
    LANGUAGE_MONGOLIAN: _ClassVar[Language]
    LANGUAGE_BOSNIAN: _ClassVar[Language]
    LANGUAGE_KAZAKH: _ClassVar[Language]
    LANGUAGE_ALBANIAN: _ClassVar[Language]
    LANGUAGE_SWAHILI: _ClassVar[Language]
    LANGUAGE_GALICIAN: _ClassVar[Language]
    LANGUAGE_MARATHI: _ClassVar[Language]
    LANGUAGE_PUNJABI: _ClassVar[Language]
    LANGUAGE_SINHALA: _ClassVar[Language]
    LANGUAGE_KHMER: _ClassVar[Language]
    LANGUAGE_SHONA: _ClassVar[Language]
    LANGUAGE_YORUBA: _ClassVar[Language]
    LANGUAGE_SOMALI: _ClassVar[Language]
    LANGUAGE_AFRIKAANS: _ClassVar[Language]
    LANGUAGE_OCCITAN: _ClassVar[Language]
    LANGUAGE_GEORGIAN: _ClassVar[Language]
    LANGUAGE_BELARUSIAN: _ClassVar[Language]
    LANGUAGE_TAJIK: _ClassVar[Language]
    LANGUAGE_SINDHI: _ClassVar[Language]
    LANGUAGE_GUJARATI: _ClassVar[Language]
    LANGUAGE_AMHARIC: _ClassVar[Language]
    LANGUAGE_YIDDISH: _ClassVar[Language]
    LANGUAGE_LAO: _ClassVar[Language]
    LANGUAGE_UZBEK: _ClassVar[Language]
    LANGUAGE_FAROESE: _ClassVar[Language]
    LANGUAGE_HAITIAN_CREOLE: _ClassVar[Language]
    LANGUAGE_PASHTO: _ClassVar[Language]
    LANGUAGE_TURKMEN: _ClassVar[Language]
    LANGUAGE_NYNORSK: _ClassVar[Language]
    LANGUAGE_MALTESE: _ClassVar[Language]
    LANGUAGE_SANSKRIT: _ClassVar[Language]
    LANGUAGE_LUXEMBOURGISH: _ClassVar[Language]
    LANGUAGE_MYANMAR: _ClassVar[Language]
    LANGUAGE_TIBETAN: _ClassVar[Language]
    LANGUAGE_TAGALOG: _ClassVar[Language]
    LANGUAGE_MALAGASY: _ClassVar[Language]
    LANGUAGE_ASSAMESE: _ClassVar[Language]
    LANGUAGE_TATAR: _ClassVar[Language]
    LANGUAGE_HAWAIIAN: _ClassVar[Language]
    LANGUAGE_LINGALA: _ClassVar[Language]
    LANGUAGE_HAUSA: _ClassVar[Language]
    LANGUAGE_BASHKIR: _ClassVar[Language]
    LANGUAGE_JAVANESE: _ClassVar[Language]
    LANGUAGE_SUNDANESE: _ClassVar[Language]
    LANGUAGE_CANTONESE: _ClassVar[Language]
    LANGUAGE_GERMAN_SWISS: _ClassVar[Language]
    LANGUAGE_ENGLISH_CA: _ClassVar[Language]
    LANGUAGE_UNDETERMINED: _ClassVar[Language]

class Confidence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONFIDENCE_UNSPECIFIED: _ClassVar[Confidence]
    CONFIDENCE_NONE: _ClassVar[Confidence]
    CONFIDENCE_LOW: _ClassVar[Confidence]
    CONFIDENCE_MEDIUM: _ClassVar[Confidence]
    CONFIDENCE_HIGH: _ClassVar[Confidence]

class Origin(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORIGIN_UNSPECIFIED: _ClassVar[Origin]
    ORIGIN_MIXTURE: _ClassVar[Origin]
    ORIGIN_WHISPER: _ClassVar[Origin]
    ORIGIN_SCRIBE: _ClassVar[Origin]
    ORIGIN_VOXTRAL: _ClassVar[Origin]
    ORIGIN_QWEN: _ClassVar[Origin]

class Commit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMMIT_UNSPECIFIED: _ClassVar[Commit]
    COMMIT_TRUE: _ClassVar[Commit]
    COMMIT_FALSE: _ClassVar[Commit]

class SignatureStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SIGNATURE_STATUS_UNSPECIFIED: _ClassVar[SignatureStatus]
    SIGNATURE_STATUS_ELIGIBLE: _ClassVar[SignatureStatus]
    SIGNATURE_STATUS_ADDED: _ClassVar[SignatureStatus]

class ResultStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_STATUS_UNSPECIFIED: _ClassVar[ResultStatus]
    RESULT_STATUS_FORMATTED: _ClassVar[ResultStatus]
    RESULT_STATUS_ERROR: _ClassVar[ResultStatus]
    RESULT_STATUS_RAW_TRANSCRIPT: _ClassVar[ResultStatus]
PLATFORM_UNSPECIFIED: Platform
PLATFORM_MACOS: Platform
PLATFORM_WIN32: Platform
PLATFORM_IOS: Platform
PLATFORM_ANDROID: Platform
PLATFORM_WEB: Platform
PLATFORM_API: Platform
APP_TYPE_UNSPECIFIED: AppType
APP_TYPE_OTHER: AppType
APP_TYPE_BROWSER: AppType
APP_TYPE_PERSONAL_MESSAGING: AppType
APP_TYPE_WORK_MESSAGING: AppType
APP_TYPE_EMAIL: AppType
APP_TYPE_CHATBOT: AppType
APP_TYPE_DEVELOPER: AppType
CHAT_ROLE_UNSPECIFIED: ChatRole
CHAT_ROLE_USER: ChatRole
CHAT_ROLE_HUMAN: ChatRole
CHAT_ROLE_ASSISTANT: ChatRole
AUDIO_ENCODING_UNSPECIFIED: AudioEncoding
AUDIO_ENCODING_WAV: AudioEncoding
AUDIO_ENCODING_OPUS: AudioEncoding
ENVIRONMENT_UNSPECIFIED: Environment
ENVIRONMENT_PRODUCTION: Environment
ENVIRONMENT_STAGING: Environment
ENVIRONMENT_DEVELOPMENT: Environment
ENVIRONMENT_TEST: Environment
WRITING_STYLE_UNSPECIFIED: WritingStyle
WRITING_STYLE_FORMAL: WritingStyle
WRITING_STYLE_CASUAL: WritingStyle
WRITING_STYLE_VERY_CASUAL: WritingStyle
WRITING_STYLE_EXCITED: WritingStyle
WRITING_STYLE_GENZ: WritingStyle
FLOW_SIGNATURE_PREFIX_UNSPECIFIED: FlowSignaturePrefix
FLOW_SIGNATURE_PREFIX_SPOKEN: FlowSignaturePrefix
FLOW_SIGNATURE_PREFIX_WRITTEN: FlowSignaturePrefix
EDITING_STRENGTH_UNSPECIFIED: EditingStrength
EDITING_STRENGTH_VERBATIM: EditingStrength
EDITING_STRENGTH_LIGHT: EditingStrength
EDITING_STRENGTH_MEDIUM: EditingStrength
EDITING_STRENGTH_HEAVY: EditingStrength
LANGUAGE_UNSPECIFIED: Language
LANGUAGE_ENGLISH_US: Language
LANGUAGE_ENGLISH_UK: Language
LANGUAGE_CHINESE_SIMPLIFIED: Language
LANGUAGE_CHINESE_TRADITIONAL: Language
LANGUAGE_GERMAN: Language
LANGUAGE_SPANISH: Language
LANGUAGE_RUSSIAN: Language
LANGUAGE_KOREAN: Language
LANGUAGE_FRENCH: Language
LANGUAGE_JAPANESE: Language
LANGUAGE_PORTUGUESE: Language
LANGUAGE_TURKISH: Language
LANGUAGE_POLISH: Language
LANGUAGE_CATALAN: Language
LANGUAGE_DUTCH: Language
LANGUAGE_ARABIC: Language
LANGUAGE_SWEDISH: Language
LANGUAGE_ITALIAN: Language
LANGUAGE_INDONESIAN: Language
LANGUAGE_HINDI: Language
LANGUAGE_HINGLISH: Language
LANGUAGE_FINNISH: Language
LANGUAGE_VIETNAMESE: Language
LANGUAGE_HEBREW: Language
LANGUAGE_UKRAINIAN: Language
LANGUAGE_GREEK: Language
LANGUAGE_MALAY: Language
LANGUAGE_CZECH: Language
LANGUAGE_ROMANIAN: Language
LANGUAGE_DANISH: Language
LANGUAGE_HUNGARIAN: Language
LANGUAGE_TAMIL: Language
LANGUAGE_NORWEGIAN: Language
LANGUAGE_THAI: Language
LANGUAGE_URDU: Language
LANGUAGE_CROATIAN: Language
LANGUAGE_BULGARIAN: Language
LANGUAGE_LITHUANIAN: Language
LANGUAGE_LATIN: Language
LANGUAGE_MAORI: Language
LANGUAGE_MALAYALAM: Language
LANGUAGE_WELSH: Language
LANGUAGE_SLOVAK: Language
LANGUAGE_TELUGU: Language
LANGUAGE_PERSIAN: Language
LANGUAGE_LATVIAN: Language
LANGUAGE_BENGALI: Language
LANGUAGE_SERBIAN: Language
LANGUAGE_AZERBAIJANI: Language
LANGUAGE_SLOVENIAN: Language
LANGUAGE_KANNADA: Language
LANGUAGE_ESTONIAN: Language
LANGUAGE_MACEDONIAN: Language
LANGUAGE_BRETON: Language
LANGUAGE_BASQUE: Language
LANGUAGE_ICELANDIC: Language
LANGUAGE_ARMENIAN: Language
LANGUAGE_NEPALI: Language
LANGUAGE_MONGOLIAN: Language
LANGUAGE_BOSNIAN: Language
LANGUAGE_KAZAKH: Language
LANGUAGE_ALBANIAN: Language
LANGUAGE_SWAHILI: Language
LANGUAGE_GALICIAN: Language
LANGUAGE_MARATHI: Language
LANGUAGE_PUNJABI: Language
LANGUAGE_SINHALA: Language
LANGUAGE_KHMER: Language
LANGUAGE_SHONA: Language
LANGUAGE_YORUBA: Language
LANGUAGE_SOMALI: Language
LANGUAGE_AFRIKAANS: Language
LANGUAGE_OCCITAN: Language
LANGUAGE_GEORGIAN: Language
LANGUAGE_BELARUSIAN: Language
LANGUAGE_TAJIK: Language
LANGUAGE_SINDHI: Language
LANGUAGE_GUJARATI: Language
LANGUAGE_AMHARIC: Language
LANGUAGE_YIDDISH: Language
LANGUAGE_LAO: Language
LANGUAGE_UZBEK: Language
LANGUAGE_FAROESE: Language
LANGUAGE_HAITIAN_CREOLE: Language
LANGUAGE_PASHTO: Language
LANGUAGE_TURKMEN: Language
LANGUAGE_NYNORSK: Language
LANGUAGE_MALTESE: Language
LANGUAGE_SANSKRIT: Language
LANGUAGE_LUXEMBOURGISH: Language
LANGUAGE_MYANMAR: Language
LANGUAGE_TIBETAN: Language
LANGUAGE_TAGALOG: Language
LANGUAGE_MALAGASY: Language
LANGUAGE_ASSAMESE: Language
LANGUAGE_TATAR: Language
LANGUAGE_HAWAIIAN: Language
LANGUAGE_LINGALA: Language
LANGUAGE_HAUSA: Language
LANGUAGE_BASHKIR: Language
LANGUAGE_JAVANESE: Language
LANGUAGE_SUNDANESE: Language
LANGUAGE_CANTONESE: Language
LANGUAGE_GERMAN_SWISS: Language
LANGUAGE_ENGLISH_CA: Language
LANGUAGE_UNDETERMINED: Language
CONFIDENCE_UNSPECIFIED: Confidence
CONFIDENCE_NONE: Confidence
CONFIDENCE_LOW: Confidence
CONFIDENCE_MEDIUM: Confidence
CONFIDENCE_HIGH: Confidence
ORIGIN_UNSPECIFIED: Origin
ORIGIN_MIXTURE: Origin
ORIGIN_WHISPER: Origin
ORIGIN_SCRIBE: Origin
ORIGIN_VOXTRAL: Origin
ORIGIN_QWEN: Origin
COMMIT_UNSPECIFIED: Commit
COMMIT_TRUE: Commit
COMMIT_FALSE: Commit
SIGNATURE_STATUS_UNSPECIFIED: SignatureStatus
SIGNATURE_STATUS_ELIGIBLE: SignatureStatus
SIGNATURE_STATUS_ADDED: SignatureStatus
RESULT_STATUS_UNSPECIFIED: ResultStatus
RESULT_STATUS_FORMATTED: ResultStatus
RESULT_STATUS_ERROR: ResultStatus
RESULT_STATUS_RAW_TRANSCRIPT: ResultStatus

class Version(_message.Message):
    __slots__ = ("major", "minor", "patch")
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    patch: int
    def __init__(self, major: _Optional[int] = ..., minor: _Optional[int] = ..., patch: _Optional[int] = ...) -> None: ...

class Client(_message.Message):
    __slots__ = ("name", "platform", "version")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    platform: Platform
    version: Version
    def __init__(self, name: _Optional[str] = ..., platform: _Optional[_Union[Platform, str]] = ..., version: _Optional[_Union[Version, _Mapping]] = ...) -> None: ...

class App(_message.Message):
    __slots__ = ("name", "bundle_id", "url", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    bundle_id: str
    url: str
    type: AppType
    def __init__(self, name: _Optional[str] = ..., bundle_id: _Optional[str] = ..., url: _Optional[str] = ..., type: _Optional[_Union[AppType, str]] = ...) -> None: ...

class Textbox(_message.Message):
    __slots__ = ("contents", "before_text", "selected_text", "after_text")
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    BEFORE_TEXT_FIELD_NUMBER: _ClassVar[int]
    SELECTED_TEXT_FIELD_NUMBER: _ClassVar[int]
    AFTER_TEXT_FIELD_NUMBER: _ClassVar[int]
    contents: str
    before_text: str
    selected_text: str
    after_text: str
    def __init__(self, contents: _Optional[str] = ..., before_text: _Optional[str] = ..., selected_text: _Optional[str] = ..., after_text: _Optional[str] = ...) -> None: ...

class DynamicVocabulary(_message.Message):
    __slots__ = ("screen_content_ax", "screen_content_ocr", "variable_names", "file_names")
    SCREEN_CONTENT_AX_FIELD_NUMBER: _ClassVar[int]
    SCREEN_CONTENT_OCR_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_NAMES_FIELD_NUMBER: _ClassVar[int]
    FILE_NAMES_FIELD_NUMBER: _ClassVar[int]
    screen_content_ax: _containers.RepeatedScalarFieldContainer[str]
    screen_content_ocr: _containers.RepeatedScalarFieldContainer[str]
    variable_names: _containers.RepeatedScalarFieldContainer[str]
    file_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, screen_content_ax: _Optional[_Iterable[str]] = ..., screen_content_ocr: _Optional[_Iterable[str]] = ..., variable_names: _Optional[_Iterable[str]] = ..., file_names: _Optional[_Iterable[str]] = ...) -> None: ...

class ChatMessage(_message.Message):
    __slots__ = ("role", "content", "sender_id")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    role: ChatRole
    content: str
    sender_id: str
    def __init__(self, role: _Optional[_Union[ChatRole, str]] = ..., content: _Optional[str] = ..., sender_id: _Optional[str] = ...) -> None: ...

class Conversation(_message.Message):
    __slots__ = ("id", "participants", "messages")
    ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    id: str
    participants: _containers.RepeatedScalarFieldContainer[str]
    messages: _containers.RepeatedCompositeFieldContainer[ChatMessage]
    def __init__(self, id: _Optional[str] = ..., participants: _Optional[_Iterable[str]] = ..., messages: _Optional[_Iterable[_Union[ChatMessage, _Mapping]]] = ...) -> None: ...

class Context(_message.Message):
    __slots__ = ("app", "textbox", "vocabulary", "user_identifier", "content_text", "content_html", "session_dictation_apps", "screenshot", "conversation")
    APP_FIELD_NUMBER: _ClassVar[int]
    TEXTBOX_FIELD_NUMBER: _ClassVar[int]
    VOCABULARY_FIELD_NUMBER: _ClassVar[int]
    USER_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TEXT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_HTML_FIELD_NUMBER: _ClassVar[int]
    SESSION_DICTATION_APPS_FIELD_NUMBER: _ClassVar[int]
    SCREENSHOT_FIELD_NUMBER: _ClassVar[int]
    CONVERSATION_FIELD_NUMBER: _ClassVar[int]
    app: App
    textbox: Textbox
    vocabulary: DynamicVocabulary
    user_identifier: str
    content_text: str
    content_html: str
    session_dictation_apps: _containers.RepeatedCompositeFieldContainer[App]
    screenshot: bytes
    conversation: Conversation
    def __init__(self, app: _Optional[_Union[App, _Mapping]] = ..., textbox: _Optional[_Union[Textbox, _Mapping]] = ..., vocabulary: _Optional[_Union[DynamicVocabulary, _Mapping]] = ..., user_identifier: _Optional[str] = ..., content_text: _Optional[str] = ..., content_html: _Optional[str] = ..., session_dictation_apps: _Optional[_Iterable[_Union[App, _Mapping]]] = ..., screenshot: _Optional[bytes] = ..., conversation: _Optional[_Union[Conversation, _Mapping]] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ("user_id", "session_id", "request_id", "audio_encoding", "environment", "client", "debug", "referral_code", "always_wait_scribe")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    AUDIO_ENCODING_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    DEBUG_FIELD_NUMBER: _ClassVar[int]
    REFERRAL_CODE_FIELD_NUMBER: _ClassVar[int]
    ALWAYS_WAIT_SCRIBE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    session_id: str
    request_id: str
    audio_encoding: AudioEncoding
    environment: Environment
    client: Client
    debug: bool
    referral_code: str
    always_wait_scribe: bool
    def __init__(self, user_id: _Optional[str] = ..., session_id: _Optional[str] = ..., request_id: _Optional[str] = ..., audio_encoding: _Optional[_Union[AudioEncoding, str]] = ..., environment: _Optional[_Union[Environment, str]] = ..., client: _Optional[_Union[Client, _Mapping]] = ..., debug: _Optional[bool] = ..., referral_code: _Optional[str] = ..., always_wait_scribe: _Optional[bool] = ...) -> None: ...

class GeneralWritingStyle(_message.Message):
    __slots__ = ("other", "personal", "work", "email")
    OTHER_FIELD_NUMBER: _ClassVar[int]
    PERSONAL_FIELD_NUMBER: _ClassVar[int]
    WORK_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    other: WritingStyle
    personal: WritingStyle
    work: WritingStyle
    email: WritingStyle
    def __init__(self, other: _Optional[_Union[WritingStyle, str]] = ..., personal: _Optional[_Union[WritingStyle, str]] = ..., work: _Optional[_Union[WritingStyle, str]] = ..., email: _Optional[_Union[WritingStyle, str]] = ...) -> None: ...

class TaggingStyle(_message.Message):
    __slots__ = ("slack",)
    SLACK_FIELD_NUMBER: _ClassVar[int]
    slack: bool
    def __init__(self, slack: _Optional[bool] = ...) -> None: ...

class SignatureStyle(_message.Message):
    __slots__ = ("flow_signature_prefix", "flow_signature_hyperlink", "sign_emails")
    FLOW_SIGNATURE_PREFIX_FIELD_NUMBER: _ClassVar[int]
    FLOW_SIGNATURE_HYPERLINK_FIELD_NUMBER: _ClassVar[int]
    SIGN_EMAILS_FIELD_NUMBER: _ClassVar[int]
    flow_signature_prefix: FlowSignaturePrefix
    flow_signature_hyperlink: bool
    sign_emails: bool
    def __init__(self, flow_signature_prefix: _Optional[_Union[FlowSignaturePrefix, str]] = ..., flow_signature_hyperlink: _Optional[bool] = ..., sign_emails: _Optional[bool] = ...) -> None: ...

class StyleConfig(_message.Message):
    __slots__ = ("general_style", "override_style", "tagging", "signature", "editing_strength")
    GENERAL_STYLE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_STYLE_FIELD_NUMBER: _ClassVar[int]
    TAGGING_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    EDITING_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    general_style: GeneralWritingStyle
    override_style: WritingStyle
    tagging: TaggingStyle
    signature: SignatureStyle
    editing_strength: EditingStrength
    def __init__(self, general_style: _Optional[_Union[GeneralWritingStyle, _Mapping]] = ..., override_style: _Optional[_Union[WritingStyle, str]] = ..., tagging: _Optional[_Union[TaggingStyle, _Mapping]] = ..., signature: _Optional[_Union[SignatureStyle, _Mapping]] = ..., editing_strength: _Optional[_Union[EditingStrength, str]] = ...) -> None: ...

class AudioPackets(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, items: _Optional[_Iterable[bytes]] = ...) -> None: ...

class AudioFile(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class Payload(_message.Message):
    __slots__ = ("audio_packets", "audio_file")
    AUDIO_PACKETS_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FILE_FIELD_NUMBER: _ClassVar[int]
    audio_packets: AudioPackets
    audio_file: AudioFile
    def __init__(self, audio_packets: _Optional[_Union[AudioPackets, _Mapping]] = ..., audio_file: _Optional[_Union[AudioFile, _Mapping]] = ...) -> None: ...

class Text(_message.Message):
    __slots__ = ("content", "num_tokens", "languages")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    NUM_TOKENS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGES_FIELD_NUMBER: _ClassVar[int]
    content: str
    num_tokens: int
    languages: _containers.RepeatedScalarFieldContainer[Language]
    def __init__(self, content: _Optional[str] = ..., num_tokens: _Optional[int] = ..., languages: _Optional[_Iterable[_Union[Language, str]]] = ...) -> None: ...

class Progress(_message.Message):
    __slots__ = ("transcriber", "transcriber_finished", "formatter", "formatter_finished", "post_processing_finished")
    TRANSCRIBER_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIBER_FINISHED_FIELD_NUMBER: _ClassVar[int]
    FORMATTER_FIELD_NUMBER: _ClassVar[int]
    FORMATTER_FINISHED_FIELD_NUMBER: _ClassVar[int]
    POST_PROCESSING_FINISHED_FIELD_NUMBER: _ClassVar[int]
    transcriber: _duration_pb2.Duration
    transcriber_finished: bool
    formatter: _duration_pb2.Duration
    formatter_finished: bool
    post_processing_finished: bool
    def __init__(self, transcriber: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., transcriber_finished: _Optional[bool] = ..., formatter: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., formatter_finished: _Optional[bool] = ..., post_processing_finished: _Optional[bool] = ...) -> None: ...

class UserActions(_message.Message):
    __slots__ = ("check_mic", "check_language")
    CHECK_MIC_FIELD_NUMBER: _ClassVar[int]
    CHECK_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    check_mic: bool
    check_language: Language
    def __init__(self, check_mic: _Optional[bool] = ..., check_language: _Optional[_Union[Language, str]] = ...) -> None: ...

class WordAlignment(_message.Message):
    __slots__ = ("word", "score")
    WORD_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    word: str
    score: float
    def __init__(self, word: _Optional[str] = ..., score: _Optional[float] = ...) -> None: ...

class CandidateBeam(_message.Message):
    __slots__ = ("text", "score", "confidence", "origin", "alignment_score", "original_text", "word_alignments")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_SCORE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_TEXT_FIELD_NUMBER: _ClassVar[int]
    WORD_ALIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    text: Text
    score: float
    confidence: Confidence
    origin: Origin
    alignment_score: float
    original_text: str
    word_alignments: _containers.RepeatedCompositeFieldContainer[WordAlignment]
    def __init__(self, text: _Optional[_Union[Text, _Mapping]] = ..., score: _Optional[float] = ..., confidence: _Optional[_Union[Confidence, str]] = ..., origin: _Optional[_Union[Origin, str]] = ..., alignment_score: _Optional[float] = ..., original_text: _Optional[str] = ..., word_alignments: _Optional[_Iterable[_Union[WordAlignment, _Mapping]]] = ...) -> None: ...

class State(_message.Message):
    __slots__ = ("progress", "raw_text", "formatted_text", "confidence", "user_actions", "candidate_beams", "audio_snr", "audio_volume", "mean_alignment_score", "formatted_raw_len")
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    RAW_TEXT_FIELD_NUMBER: _ClassVar[int]
    FORMATTED_TEXT_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    USER_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_BEAMS_FIELD_NUMBER: _ClassVar[int]
    AUDIO_SNR_FIELD_NUMBER: _ClassVar[int]
    AUDIO_VOLUME_FIELD_NUMBER: _ClassVar[int]
    MEAN_ALIGNMENT_SCORE_FIELD_NUMBER: _ClassVar[int]
    FORMATTED_RAW_LEN_FIELD_NUMBER: _ClassVar[int]
    progress: Progress
    raw_text: Text
    formatted_text: Text
    confidence: Confidence
    user_actions: UserActions
    candidate_beams: _containers.RepeatedCompositeFieldContainer[CandidateBeam]
    audio_snr: float
    audio_volume: float
    mean_alignment_score: float
    formatted_raw_len: int
    def __init__(self, progress: _Optional[_Union[Progress, _Mapping]] = ..., raw_text: _Optional[_Union[Text, _Mapping]] = ..., formatted_text: _Optional[_Union[Text, _Mapping]] = ..., confidence: _Optional[_Union[Confidence, str]] = ..., user_actions: _Optional[_Union[UserActions, _Mapping]] = ..., candidate_beams: _Optional[_Iterable[_Union[CandidateBeam, _Mapping]]] = ..., audio_snr: _Optional[float] = ..., audio_volume: _Optional[float] = ..., mean_alignment_score: _Optional[float] = ..., formatted_raw_len: _Optional[int] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("first_name", "last_name", "email")
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    email: str
    def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class StaticVocabulary(_message.Message):
    __slots__ = ("dictionary_personal", "dictionary_team", "dictionary_personal_starred", "dictionary_team_starred")
    DICTIONARY_PERSONAL_FIELD_NUMBER: _ClassVar[int]
    DICTIONARY_TEAM_FIELD_NUMBER: _ClassVar[int]
    DICTIONARY_PERSONAL_STARRED_FIELD_NUMBER: _ClassVar[int]
    DICTIONARY_TEAM_STARRED_FIELD_NUMBER: _ClassVar[int]
    dictionary_personal: _containers.RepeatedScalarFieldContainer[str]
    dictionary_team: _containers.RepeatedScalarFieldContainer[str]
    dictionary_personal_starred: _containers.RepeatedScalarFieldContainer[str]
    dictionary_team_starred: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dictionary_personal: _Optional[_Iterable[str]] = ..., dictionary_team: _Optional[_Iterable[str]] = ..., dictionary_personal_starred: _Optional[_Iterable[str]] = ..., dictionary_team_starred: _Optional[_Iterable[str]] = ...) -> None: ...

class Replacements(_message.Message):
    __slots__ = ("replacements_personal", "replacements_team", "snippets_personal", "snippets_team")
    class ReplacementsPersonalEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class ReplacementsTeamEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SnippetsPersonalEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SnippetsTeamEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    REPLACEMENTS_PERSONAL_FIELD_NUMBER: _ClassVar[int]
    REPLACEMENTS_TEAM_FIELD_NUMBER: _ClassVar[int]
    SNIPPETS_PERSONAL_FIELD_NUMBER: _ClassVar[int]
    SNIPPETS_TEAM_FIELD_NUMBER: _ClassVar[int]
    replacements_personal: _containers.ScalarMap[str, str]
    replacements_team: _containers.ScalarMap[str, str]
    snippets_personal: _containers.ScalarMap[str, str]
    snippets_team: _containers.ScalarMap[str, str]
    def __init__(self, replacements_personal: _Optional[_Mapping[str, str]] = ..., replacements_team: _Optional[_Mapping[str, str]] = ..., snippets_personal: _Optional[_Mapping[str, str]] = ..., snippets_team: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Preferences(_message.Message):
    __slots__ = ("user", "language", "vocabulary", "replacements", "style_config")
    USER_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    VOCABULARY_FIELD_NUMBER: _ClassVar[int]
    REPLACEMENTS_FIELD_NUMBER: _ClassVar[int]
    STYLE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    user: User
    language: _containers.RepeatedScalarFieldContainer[Language]
    vocabulary: StaticVocabulary
    replacements: Replacements
    style_config: StyleConfig
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., language: _Optional[_Iterable[_Union[Language, str]]] = ..., vocabulary: _Optional[_Union[StaticVocabulary, _Mapping]] = ..., replacements: _Optional[_Union[Replacements, _Mapping]] = ..., style_config: _Optional[_Union[StyleConfig, _Mapping]] = ...) -> None: ...

class Init(_message.Message):
    __slots__ = ("metadata", "preferences", "state")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    metadata: Metadata
    preferences: Preferences
    state: State
    def __init__(self, metadata: _Optional[_Union[Metadata, _Mapping]] = ..., preferences: _Optional[_Union[Preferences, _Mapping]] = ..., state: _Optional[_Union[State, _Mapping]] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ("init", "context", "payload", "commit")
    INIT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    init: Init
    context: Context
    payload: Payload
    commit: Commit
    def __init__(self, init: _Optional[_Union[Init, _Mapping]] = ..., context: _Optional[_Union[Context, _Mapping]] = ..., payload: _Optional[_Union[Payload, _Mapping]] = ..., commit: _Optional[_Union[Commit, str]] = ...) -> None: ...

class ResponseTime(_message.Message):
    __slots__ = ("transcribe", "transcribe_overhead", "format", "format_overhead", "post_process", "total", "external_asr_time", "external_llm_time", "generate_queue_duration", "generate_work_duration")
    TRANSCRIBE_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIBE_OVERHEAD_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    FORMAT_OVERHEAD_FIELD_NUMBER: _ClassVar[int]
    POST_PROCESS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ASR_TIME_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_LLM_TIME_FIELD_NUMBER: _ClassVar[int]
    GENERATE_QUEUE_DURATION_FIELD_NUMBER: _ClassVar[int]
    GENERATE_WORK_DURATION_FIELD_NUMBER: _ClassVar[int]
    transcribe: _duration_pb2.Duration
    transcribe_overhead: _duration_pb2.Duration
    format: _duration_pb2.Duration
    format_overhead: _duration_pb2.Duration
    post_process: _duration_pb2.Duration
    total: _duration_pb2.Duration
    external_asr_time: _duration_pb2.Duration
    external_llm_time: _duration_pb2.Duration
    generate_queue_duration: _duration_pb2.Duration
    generate_work_duration: _duration_pb2.Duration
    def __init__(self, transcribe: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., transcribe_overhead: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., format: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., format_overhead: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., post_process: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., total: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., external_asr_time: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., external_llm_time: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., generate_queue_duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., generate_work_duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class Transcription(_message.Message):
    __slots__ = ("html", "plaintext", "num_tokens", "languages", "confidence", "language_detection_low_confidence")
    HTML_FIELD_NUMBER: _ClassVar[int]
    PLAINTEXT_FIELD_NUMBER: _ClassVar[int]
    NUM_TOKENS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGES_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_DETECTION_LOW_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    html: str
    plaintext: str
    num_tokens: int
    languages: _containers.RepeatedScalarFieldContainer[Language]
    confidence: float
    language_detection_low_confidence: bool
    def __init__(self, html: _Optional[str] = ..., plaintext: _Optional[str] = ..., num_tokens: _Optional[int] = ..., languages: _Optional[_Iterable[_Union[Language, str]]] = ..., confidence: _Optional[float] = ..., language_detection_low_confidence: _Optional[bool] = ...) -> None: ...

class TranscriptionStats(_message.Message):
    __slots__ = ("word_deletions", "context_word_count", "word_substitutions")
    WORD_DELETIONS_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_WORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    WORD_SUBSTITUTIONS_FIELD_NUMBER: _ClassVar[int]
    word_deletions: int
    context_word_count: int
    word_substitutions: int
    def __init__(self, word_deletions: _Optional[int] = ..., context_word_count: _Optional[int] = ..., word_substitutions: _Optional[int] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ("output", "audio_duration", "response_time", "signature_status", "status", "stats", "transcript_origin", "server_address", "format_skip_reason")
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    AUDIO_DURATION_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    SERVER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    FORMAT_SKIP_REASON_FIELD_NUMBER: _ClassVar[int]
    output: Transcription
    audio_duration: _duration_pb2.Duration
    response_time: ResponseTime
    signature_status: SignatureStatus
    status: ResultStatus
    stats: TranscriptionStats
    transcript_origin: str
    server_address: str
    format_skip_reason: str
    def __init__(self, output: _Optional[_Union[Transcription, _Mapping]] = ..., audio_duration: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ..., response_time: _Optional[_Union[ResponseTime, _Mapping]] = ..., signature_status: _Optional[_Union[SignatureStatus, str]] = ..., status: _Optional[_Union[ResultStatus, str]] = ..., stats: _Optional[_Union[TranscriptionStats, _Mapping]] = ..., transcript_origin: _Optional[str] = ..., server_address: _Optional[str] = ..., format_skip_reason: _Optional[str] = ...) -> None: ...

class Heartbeat(_message.Message):
    __slots__ = ("audio_received_seconds", "commit_ack")
    AUDIO_RECEIVED_SECONDS_FIELD_NUMBER: _ClassVar[int]
    COMMIT_ACK_FIELD_NUMBER: _ClassVar[int]
    audio_received_seconds: float
    commit_ack: bool
    def __init__(self, audio_received_seconds: _Optional[float] = ..., commit_ack: _Optional[bool] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("result", "state", "all_states", "heartbeat")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ALL_STATES_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    state: State
    all_states: _containers.RepeatedCompositeFieldContainer[State]
    heartbeat: Heartbeat
    def __init__(self, result: _Optional[_Union[Result, _Mapping]] = ..., state: _Optional[_Union[State, _Mapping]] = ..., all_states: _Optional[_Iterable[_Union[State, _Mapping]]] = ..., heartbeat: _Optional[_Union[Heartbeat, _Mapping]] = ...) -> None: ...
