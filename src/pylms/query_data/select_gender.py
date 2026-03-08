"""Utility for selecting students by gender."""

import polars as pl

from ..constants import GENDER, NAME, SERIAL
from ..data import DataStore
from ..errors import Result


def select_gender(ds: DataStore, gender: str) -> Result[list[tuple[int, str]]]:
    """Select students by gender.
    
    Args:
        ds (DataStore): DataStore containing student data.
        gender (str): Gender to filter by (e.g., "Male", "Female").
        
    Returns:
        Result[list[tuple[int, str]]]: Success with list of (serial, name) tuples or error.
    """
    try:
        # Get reference to underlying DataFrame
        data = ds.as_ref()
        
        # Filter by gender (case-insensitive comparison)
        filtered = data.filter(pl.col(GENDER).str.to_lowercase() == gender.lower())
        
        if filtered.height == 0:
            return Result.err(f"No students found with gender '{gender}'")
        
        # Extract serial and name tuples
        results = [(filtered[i, SERIAL], filtered[i, NAME]) for i in range(filtered.height)]
        return Result.ok(results)
    except Exception as e:
        return Result.err(f"Error filtering by gender: {str(e)}")
