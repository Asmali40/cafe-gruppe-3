""Konstanten für den Router."""

from typing import Final

__all__ = [
    "ETAG",
    "IF_MATCH",
    "IF_MATCH_MIN_LEN",
    "IF_NONE_MATCH",
    "IF_NONE_MATCH_MIN_LEN",
]

ETAG: Final = "ETag"
IF_MATCH: Final = "if-match"
IF_MATCH_MIN_LEN: Final = 3
IF_NONE_MATCH: Final = "if-none-match"
IF_NONE_MATCH_MIN_LEN: Final = 3
