"""Email input type selector."""

from enum import Enum, auto


class EmailInputMode(Enum):
    """Types of email input methods."""

    TXT = auto()
    CSV = auto()
    EXCEL = auto()
    STRING = auto()
