"""Utility for selecting students by internship category."""

import polars as pl

from ..constants import INTERNSHIP, NAME, SERIAL
from ..data import DataStore
from ..errors import Result


def select_internship(ds: DataStore, category: str) -> Result[list[tuple[int, str]]]:
    """Select students by internship category.
    
    Args:
        ds (DataStore): DataStore containing student data.
        category (str): Category to filter by (e.g., "NYSC", "1 MONTH SIWES").
        
    Returns:
        Result[list[tuple[int, str]]]: Success with list of (serial, name) tuples or error.
    """
    try:
        # Get reference to underlying DataFrame
        data = ds.as_ref()
        
        # Filter by exact internship category match
        filtered = data.filter(pl.col(INTERNSHIP) == category)
        
        if filtered.height == 0:
            return Result.err(f"No students found in category '{category}'")
        
        # Extract serial and name tuples
        results: list[tuple[int, str]] = [(filtered[i, SERIAL], filtered[i, NAME]) for i in range(filtered.height)]
        return Result.ok(results)
    except Exception as e:
        return Result.err(f"Error filtering by internship: {str(e)}")
