"""Pipeline for chaining multiple selectors to filter students."""

import polars as pl

from ..constants import NAME, SERIAL
from ..data import DataStore
from ..errors import Result
from .print_selection import print_selection
from .search_completion import search_completion
from .search_gender import search_gender
from .search_internship import search_internship
from .search_name import search_name
from .search_serials import search_serials
from .selector_type import Selector


def apply_selector_pipeline(
    ds: DataStore,
    selectors: list[Selector],
) -> Result[list[int]]:
    """Apply a pipeline of selectors to progressively filter students.
    
    Each selector is invoked based on its type, receives the current DataStore,
    and returns a list of serial numbers. The pipeline creates a new filtered
    DataStore after each selector and passes it to the next selector.
    
    Args:
        ds (DataStore): Initial DataStore containing all student data.
        selectors (list[Selector]): List of selector types to apply.
        
    Returns:
        Result[list[int]]: Success with final filtered serial numbers or error.
    """
    if len(selectors) == 0:
        return Result.err("No selectors provided")
    
    # Map selector types to their corresponding search functions
    selector_map = {
        Selector.NAME: search_name,
        Selector.SERIALS: search_serials,
        Selector.INTERNSHIP: search_internship,
        Selector.COMPLETION: search_completion,
        Selector.GENDER: search_gender,
    }
    
    current_ds = ds
    
    # Apply each selector sequentially
    for _, selector_type in enumerate(selectors):
        # Get the search function for this selector type
        search_fn = selector_map.get(selector_type)
        if search_fn is None:
            return Result.err(f"Unknown selector type: {selector_type}")
        
        # Execute the search function
        result = search_fn(current_ds)
        if result.is_err():
            return result.propagate()
        
        serials = result.unwrap()
        
        # Filter DataStore to only include selected serials
        data = current_ds.as_ref()
        filtered = data.filter(pl.col(SERIAL).is_in(serials))
        
        # Create new DataStore with filtered data
        current_ds = DataStore(filtered)
        
        # Display current selection
        selections = [(filtered[j, SERIAL], filtered[j, NAME]) for j in range(filtered.height)]
        print_selection(selections)
    
    # Check if any students remain after all filters
    final_data = current_ds.as_ref()
    if final_data.height == 0:
        return Result.err("No students remaining after all filters")
    
    # Extract final serial numbers
    final_serials: list[int] = final_data.select(SERIAL).to_series().to_list()
    
    return Result.ok(final_serials)
