"""Interactive search for students by completion date."""

from ..cli import input_str
from ..data import DataStore
from ..errors import ForcedExitError, Result
from ..info import print_info, printpass
from .print_selection import print_selection
from .select_completion import select_completion


def search_completion(ds: DataStore) -> Result[list[int]]:
    """Search for students by completion date.
    
    Loops until successful selection or ForcedExitError.
    
    Args:
        ds (DataStore): DataStore containing student data.
        
    Returns:
        Result[list[int]]: Success with selected serial numbers or ForcedExitError.
    """
    while True:
        print_info("Enter completion (e.g., 'June', '6', or 'June,July')")
        result = input_str("Completion: ", lower_case=False)
        if result.is_err():
            err = result.unwrap_err()
            if isinstance(err, ForcedExitError):
                return result.propagate()
            result.print_if_err()
            continue
        
        query = result.unwrap()
        
        filter_result = select_completion(ds, query)
        if filter_result.is_err():
            filter_result.print_if_err()
            continue
        
        selections = filter_result.unwrap()
        print_info(f"Found {len(selections)} student(s) with completion '{query}'")
        print_selection(selections)
        
        printpass(f"Selected {len(selections)} student(s) with completion '{query}'")
        return Result.ok([serial for serial, _ in selections])
