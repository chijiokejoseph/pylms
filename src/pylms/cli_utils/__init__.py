"""
UTILS Package a subpackage of the src.cli package.

This package aggregates utility functions related to date string parsing, validation,
response parsing, and serial parsing used throughout the CLI components of the pylms project.

Exports:
- parse_to_serials: Function to parse serial numbers from strings.
- parse_response: Function to parse user responses from menu selections.
- parse_to_dates: Function to parse date strings into lists of dates.
- val_date_str: Function to validate date strings.
"""

from .date_strings_parse import parse_to_dates
from .date_strings_verify import val_date_str
from .email_test import validate_email
from .response_parser import parse_response
from .serial_parser import parse_to_serials

__all__ = [
    "parse_to_serials",
    "parse_response",
    "parse_to_dates",
    "val_date_str",
    "validate_email",
]
