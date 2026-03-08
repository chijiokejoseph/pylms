"""Interactive functions for user-driven student selection."""

from ..cli import input_option
from ..data import DataStore
from ..errors import Result
from .pipeline import apply_selector_pipeline
from .search_completion import search_completion
from .search_gender import search_gender
from .search_internship import search_internship
from .search_name import search_name
from .search_path import search_path
from .search_serials import search_serials
from .selector_type import Selector


def search_data(ds: DataStore) -> Result[list[int]]:
    """Interactive function to select students using various search methods.

    Provides user with options to:
    1. Search by name
    2. Search by serial numbers
    3. Search by internship category
    4. Search by completion date
    5. Search by gender
    6. Combined search (apply multiple filters)

    Args:
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[list[int]]: Success with list of selected serial numbers or ForcedExitError.
    """
    options = [
        "Search by name",
        "Search by serial numbers",
        "Search by internship category",
        "Search by completion date",
        "Search by gender",
        "Search by Path",
        "Combined search (multiple filters)",
    ]

    result = input_option(options, prompt="How would you like to select students?")
    if result.is_err():
        return result.propagate()

    idx, _ = result.unwrap()

    match idx:
        case 1:
            return search_name(ds)
        case 2:
            return search_serials(ds)
        case 3:
            return search_internship(ds)
        case 4:
            return search_completion(ds)
        case 5:
            return search_gender(ds)
        case 6:
            return search_path(ds)
        case 7:
            return combined_search(ds)
        case _:
            return Result.err("Invalid selection")


def combined_search(ds: DataStore) -> Result[list[int]]:
    """Interactive combined search using multiple filters.

    Args:
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[list[int]]: Success with selected serial numbers or ForcedExitError.
    """
    options = [
        "Name",
        "Serial numbers",
        "Internship category",
        "Completion date",
        "Gender",
    ]

    selector_map = [
        Selector.NAME,
        Selector.SERIALS,
        Selector.INTERNSHIP,
        Selector.COMPLETION,
        Selector.GENDER,
    ]

    selectors: list[Selector] = []

    while True:
        result = input_option(
            options, prompt="Select a filter to add (or quit to finish)"
        )
        if result.is_err():
            if len(selectors) > 0:
                break
            return result.propagate()

        idx, _ = result.unwrap()
        selector = selector_map[idx - 1]
        selectors.append(selector)
        _ = options.pop(idx)
        _ = selector_map.pop(idx)

    if len(selectors) == 0:
        return Result.err("No filters selected")

    return apply_selector_pipeline(ds, selectors)
