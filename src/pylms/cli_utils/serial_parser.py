from ..errors import Result
from .int_str_parse import parse_int_str


def parse_to_serials(entry: str) -> Result[list[int]]:
    """parse a string to a list of integers representing serial numbers.
    The string can be a single number, a comma-separated list of numbers,
    a range of numbers, or a combination of these formats.

    :param entry: (str) - The input string to parse.
    :type entry: str

    :return: (Result[list[int]]) - A list of integers representing the parsed serial numbers.
    :rtype: Result[list[int]]

    """

    return parse_int_str(entry)
