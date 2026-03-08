"""Utility for selecting students by name."""

import polars as pl

from ..constants import NAME, SERIAL
from ..data import DataStore
from ..errors import Result


def select_name(ds: DataStore, query: str) -> Result[list[tuple[int, str]]]:
    """Select students whose names contain the query string.
    
    Args:
        ds (DataStore): DataStore containing student data.
        query (str): Search string to match against student names.
        
    Returns:
        Result[list[tuple[int, str]]]: Success with list of (serial, name) tuples or error.
    """
    if len(query.strip()) == 0:
        return Result.err("Query string cannot be empty")
    
    try:
        # Get reference to underlying DataFrame
        data = ds.as_ref()
        query_lower = query.lower().strip()
        
        # Filter names containing query string (case-insensitive)
        matches = data.filter(
            pl.col(NAME).str.to_lowercase().str.contains(query_lower)
        )
        
        if matches.height == 0:
            return Result.err(f"No names found matching '{query}'")
        
        # Extract serial and name tuples
        results = [
            (matches[i, SERIAL], matches[i, NAME])
            for i in range(matches.height)
        ]
        
        return Result.ok(results)
    except Exception as e:
        return Result.err(f"Error querying names: {str(e)}")
