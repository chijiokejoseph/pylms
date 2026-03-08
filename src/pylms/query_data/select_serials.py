"""Utility for selecting students by serial numbers."""

from ..constants import NAME
from ..data import DataStore
from ..errors import Result


def select_serials(
    ds: DataStore, serials: list[int]
) -> Result[list[tuple[int, str]]]:
    """Select students by their serial numbers.
    
    Args:
        ds (DataStore): DataStore containing student data.
        serials (list[int]): List of serial numbers to select.
        
    Returns:
        Result[list[tuple[int, str]]]: Success with list of (serial, name) tuples or error.
    """
    if len(serials) == 0:
        return Result.err("Serial numbers list cannot be empty")
    
    try:
        # Get reference to underlying DataFrame
        data = ds.as_ref()
        max_serial = data.height
        
        # Validate all serials are within valid range (1 to max_serial)
        invalid_serials = [s for s in serials if s < 1 or s > max_serial]
        if len(invalid_serials) > 0:
            return Result.err(
                f"Invalid serial numbers: {invalid_serials}. Valid range: 1-{max_serial}"
            )
        
        # Extract names for each serial (convert to 0-based index)
        results = [(serial, data[serial - 1, NAME]) for serial in serials]
        
        return Result.ok(results)
    except Exception as e:
        return Result.err(f"Error selecting by serials: {str(e)}")
