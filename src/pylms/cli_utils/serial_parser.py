from ..errors import Result
from .int_str_parse import parse_int_str


def parse_to_serials(entry: str) -> Result[list[int]]:
    """Parse a string into a list of serial integer values.

    Accepts an input string that may represent serial numbers using a single
    number, a comma-separated list of numbers, ranges (e.g. "1-5"), or a
    combination of these formats. This function delegates the parsing work to
    `parse_int_str` and returns its `Result`.

    Args:
        entry (str): The input string encoding one or more serial numbers.

    Returns:
        Result[list[int]]: Ok containing a list of parsed integers when
            parsing succeeds, or an Err with a diagnostic message when parsing
            fails.
    """
    return parse_int_str(entry)
