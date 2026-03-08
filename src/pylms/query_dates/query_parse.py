"""Parse query strings to extract date selection criteria."""

import re

from ..errors import Result, Unit
from .selector_type import DateSelector


def _add_selector(selectors: list[DateSelector], new: DateSelector) -> Result[Unit]:
    if new == DateSelector.HELD and DateSelector.UNHELD in selectors:
        return Result.err("Cannot specify both 'held' and 'unheld'")
    
    if new == DateSelector.UNHELD and DateSelector.HELD in selectors:
            return Result.err("Cannot specify both 'held' and 'unheld'")
    

    if new == DateSelector.MARKED and DateSelector.UNMARKED in selectors:
        return Result.err("Cannot specify both 'marked' and 'unmarked'")

    if new == DateSelector.UNMARKED and DateSelector.MARKED in selectors:
        return Result.err("Cannot specify both 'marked' and 'unmarked'")

    selectors.append(new)
    return Result.unit()


def query_parse(query: str) -> Result[list[DateSelector]]:
    """Parse query string and return matching date selectors.
    
    Parses a query string separated by commas or semicolons. Each token is classified as:
    - HELD if it matches "held" (case-insensitive)
    - UNHELD if it matches "unheld" (case-insensitive)
    - MARKED if it matches "marked" (case-insensitive)
    - UNMARKED if it matches "unmarked" (case-insensitive)
    - WEEKDAY if it matches "weekday" (case-insensitive)
    
    All matching selectors from all tokens are combined.
    
    Args:
        query (str): Query string with comma or semicolon separated tokens.
        
    Returns:
        Result[list[DateSelector]]: Success with list of matching selectors or error.
    """
    # Split query by commas or semicolons
    tokens = re.split(r'[,;]', query)
    tokens = [t.strip() for t in tokens if len(t.strip()) > 0]
    
    # Check for empty query
    if len(tokens) == 0:
        return Result.err("Empty query")
    
    # Process each token
    selectors: list[DateSelector] = []
    
    for token in tokens:
        # Match token to selector type
        match True:
            case _ if re.fullmatch(r'held', token, re.IGNORECASE):
                result = _add_selector(selectors, DateSelector.HELD)
            
            case _ if re.fullmatch(r'unheld', token, re.IGNORECASE):
                result = _add_selector(selectors, DateSelector.UNHELD)
            
            case _ if re.fullmatch(r'marked', token, re.IGNORECASE):
                result = _add_selector(selectors, DateSelector.MARKED)
            
            case _ if re.fullmatch(r'unmarked', token, re.IGNORECASE):
                result = _add_selector(selectors, DateSelector.UNMARKED)
            
            case _ if re.fullmatch(r'weekday', token, re.IGNORECASE):
                result = _add_selector(selectors, DateSelector.WEEKDAY)
            
            case _:
                # Ignore unrecognized tokens
                continue

        if result.is_err():
            return result.propagate()
    
    # Check if any selectors were found
    if len(selectors) == 0:
        return Result.err("No valid date selectors matched the query")
    
    return Result.ok(selectors)
