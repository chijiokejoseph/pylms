
from pylms.cli.utils.int_str_parse import _parse_int_str


def parse_to_serials(entry: str) -> list[int]:
    """parse a string to a list of integers representing serial numbers.    
    The string can be a single number, a comma-separated list of numbers,
    a range of numbers, or a combination of these formats.
    
    :param entry: (str) - The input string to parse.
    :type entry: str
    
    :return: (list[int]) - A list of integers representing the parsed serial numbers.
    :rtype: list[int]
    
    :raises InvalidSelectionInputError: If the input string does not match any of the required formats.
    """
    
    return _parse_int_str(entry)