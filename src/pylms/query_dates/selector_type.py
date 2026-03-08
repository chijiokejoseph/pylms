"""Enum for date selector types."""

from enum import Enum, auto


class DateSelector(Enum):
    """Enumeration for date selection types."""
    
    HELD = auto()
    UNHELD = auto()
    MARKED = auto()
    UNMARKED = auto()
    WEEKDAY = auto()
