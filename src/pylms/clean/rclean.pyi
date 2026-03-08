"""Type stubs for pylms.clean.rclean module."""

from datetime import date, datetime

import polars as pl

def clean_names(names: pl.Series) -> pl.Series:
    """Clean and format student names.

    Formats names to title case, handles comma/space delimiters,
    and normalizes Arabic apostrophes.

    Args:
        names (pl.Series): List of student names to clean as polars series.

    Returns:
        pl.Series: List of cleaned and formatted names.
    """
    pass

def clean_date(input: str | date | datetime, format: str, day_first: bool) -> str:
    """Format date string or datetime object to specified format.

    Args:
        input (str | date | datetime,): Date as string, date, or datetime object.
        format (str): Target date format string (e.g., "%d/%m/%Y").
        day_first (bool): Whether day comes first in string input parsing.

    Returns:
        Formatted date string.
    """
    pass

def clean_dates(dates: pl.Series, format: str, day_first: bool) -> pl.Series:
    """Clean and format a Polars Series of dates.

    Args:
        dates (pl.Series): Polars Series containing date values.
        format (str): Target date format string (e.g., "%d/%m/%Y").
        day_first (bool): Whether day comes first in string input parsing.

    Returns:
        Polars Series with cleaned and formatted dates.
    """
    pass
