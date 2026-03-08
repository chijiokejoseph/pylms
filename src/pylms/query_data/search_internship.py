"""Interactive search for students by internship category."""

from ..cli import input_option
from ..constants import PROGRAMS
from ..data import DataStore
from ..errors import ForcedExitError, Result
from ..info import print_info, printpass
from .print_selection import print_selection
from .select_internship import select_internship


def search_internship(ds: DataStore) -> Result[list[int]]:
    """Search for students by internship category.
    
    Loops until successful selection or ForcedExitError.
    
    Args:
        ds (DataStore): DataStore containing student data.
        
    Returns:
        Result[list[int]]: Success with selected serial numbers or ForcedExitError.
    """
    while True:
        result = input_option(PROGRAMS, prompt="Select internship category")
        if result.is_err():
            err = result.unwrap_err()
            if isinstance(err, ForcedExitError):
                return result.propagate()
            result.print_if_err()
            continue
        
        _, category = result.unwrap()
        
        filter_result = select_internship(ds, category)
        if filter_result.is_err():
            filter_result.print_if_err()
            continue
        
        selections = filter_result.unwrap()
        print_info(f"Found {len(selections)} student(s) in category '{category}'")
        print_selection(selections)
        
        printpass(f"Selected {len(selections)} student(s) from category '{category}'")
        return Result.ok([serial for serial, _ in selections])
