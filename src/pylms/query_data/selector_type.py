"""Enum for selector types."""

from enum import Enum, auto


class Selector(Enum):
    """Types of student selectors available."""
    
    NAME = auto()
    SERIALS = auto()
    INTERNSHIP = auto()
    COMPLETION = auto()
    GENDER = auto()
