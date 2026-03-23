"""Utility for selecting students by completion date."""

import polars as pl

from ..cli_utils import parse_month
from ..constants import COMPLETION, COMPLETION_FMT, NAME, SERIAL
from ..data import DataStore
from ..errors import Result


def select_completion(ds: DataStore, query: str) -> Result[list[tuple[int, str]]]:
    """Select students by completion date.
    
    Supports matching by:
    - Month name: "June", "june"
    - Month number: "06", "6"
    - Multiple months: "June, July", "6,7"
    
    Args:
        ds (DataStore): DataStore containing student data.
        query (str): Completion query (month name, month number, or comma-separated).
        
    Returns:
        Result[list[tuple[int, str]]]: Success with list of (serial, name) tuples or error.
    """
    try:
        # Get reference to underlying DataFrame
        data = ds.as_ref()
        
        # Parse completion dates from string to datetime
        data = data.with_columns(
            pl.col(COMPLETION).str.strptime(pl.Date, format=COMPLETION_FMT).alias("completion_dt")
        )
        
        # Parse query string to month numbers
        month_result = parse_month(query)
        if month_result.is_err():
            return month_result.propagate()
        
        # Filter by month numbers using datetime comparison
        month_nums = month_result.unwrap()
        filtered = data.filter(pl.col("completion_dt").dt.month().is_in(month_nums))
        
        if filtered.height == 0:
            return Result.err(f"No students found with completion '{query}'")
        
        # Extract serial and name tuples
        results: list[tuple[int, str]] = [(filtered[i, SERIAL], filtered[i, NAME]) for i in range(filtered.height)]
        return Result.ok(results)
    except Exception as e:
        return Result.err(f"Error filtering by completion: {str(e)}")
