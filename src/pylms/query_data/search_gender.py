"""Interactive search for students by gender."""

from ..cli import input_option
from ..data import DataStore
from ..errors import ForcedExitError, Result
from ..info import print_info, printpass
from .print_selection import print_selection
from .select_gender import select_gender


def search_gender(ds: DataStore) -> Result[list[int]]:
    """Search for students by gender.
    
    Loops until successful selection or ForcedExitError.
    
    Args:
        ds (DataStore): DataStore containing student data.
        
    Returns:
        Result[list[int]]: Success with selected serial numbers or ForcedExitError.
    """
    while True:
        result = input_option(["Male", "Female"], prompt="Select gender")
        if result.is_err():
            err = result.unwrap_err()
            if isinstance(err, ForcedExitError):
                return result.propagate()
            result.print_if_err()
            continue
        
        _, gender = result.unwrap()
        
        filter_result = select_gender(ds, gender)
        if filter_result.is_err():
            filter_result.print_if_err()
            continue
        
        selections = filter_result.unwrap()
        print_info(f"Found {len(selections)} {gender} student(s)")
        print_selection(selections)
        
        printpass(f"Selected {len(selections)} {gender} student(s)")
        return Result.ok([serial for serial, _ in selections])
