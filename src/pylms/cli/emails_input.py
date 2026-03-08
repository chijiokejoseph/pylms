"""Backward-compatible wrapper for email input."""

from ..errors import Result
from .emails_query import query_emails


def provide_emails() -> Result[list[str]]:
    """Collect email addresses using query-based or interactive input.
    
    This function wraps query_emails for backward compatibility.
    
    Returns:
        Result[list[str]]: List of valid emails or error.
    """
    return query_emails()
