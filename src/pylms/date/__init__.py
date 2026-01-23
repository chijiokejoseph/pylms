from datetime import datetime

from dateutil.parser import parse

from .features import (
    det_week_num,
    det_year,
    to_day_num,
    to_unique_week_nums,
    to_week_num,
    to_week_nums,
)
from .parser import parse_dates, to_date


def format_date(
    date_var: str | datetime, str_format: str, day_first: bool = True
) -> str:
    """Format date to string with specified format.
    
    Args:
        date_var (str | datetime): Date string or datetime object.
        str_format (str): Target format string.
        day_first (bool): Whether to parse string dates with day first. Defaults to True.
        
    Returns:
        str: Formatted date string.
    """
    if isinstance(date_var, str):
        # Parse string then format
        return parse(date_var, dayfirst=day_first).strftime(str_format)
    else:
        # Format datetime directly
        return date_var.strftime(str_format)


def format_form_timestamp(date_var: str | datetime, str_format: str) -> str:
    """Format date for form timestamps with day-first parsing.
    
    Args:
        date_var (str | datetime): Date string or datetime object.
        str_format (str): Target format string.
        
    Returns:
        str: Formatted date string with day-first parsing.
    """
    return format_date(date_var, str_format, True)


__all__ = [
    "det_week_num",
    "det_year",
    "to_week_num",
    "to_week_nums",
    "to_unique_week_nums",
    "to_day_num",
    "format_date",
    "format_form_timestamp",
    "parse_dates",
    "to_date",
]
