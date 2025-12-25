"""CLI utilities package for common parsing and validation helpers.

This package contains small, focused utility functions used by the CLI
subsystem of pylms. Utilities include parsing and validating date strings,
parsing integer/serial ranges, email validation helpers, and general response
parsing helpers used by interactive prompts.

Exports are chosen to provide a compact API for CLI modules:
- `parse_to_serials` — parse text like "1,3,5" or "1-3" into integers
- `parse_response` — map user menu input to structured responses
- `parse_to_dates` — parse date selectors into lists of date strings
- `val_date_str` — validate a single date string
- `validate_email` — utility used in tests and CLI validation
"""

from .class_dates import parse_class_dates
from .class_nums import parse_class_nums
from .class_parser import parse_classes
from .class_verify import verify_class
from .email_verify import verify_email

__all__ = [
    "parse_class_dates",
    "parse_class_nums",
    "parse_classes",
    "verify_class",
    "verify_email",
]
