import re

from ..constants import COMMA, COMMA_DELIM, HYPHEN
from ..errors import Result, eprint


def parse_class_nums(entry: str) -> Result[list[int]]:
    """Parse a string into a list of integers (supports ranges and lists).

    Accepts single numbers, comma-separated lists, ranges (for example
    "1-5"), or combinations of these formats. Parsing returns a Result
    containing the parsed integers when successful. When input contains
    invalid formatting a `Result.err` with a diagnostic message is returned.

    Args:
        entry (str): Input string representing one or more integer selections.

    Returns:
        Result[list[int]]: Ok with the parsed list of integers, or Err with a
            diagnostic message when parsing fails.
    """

    match str(entry):
        # matches "1", "12", "13", etc.,
        case _ if re.fullmatch(r"^\d+$", entry):
            choice: int = int(entry)
            return Result.ok([choice])

        # matches "1, 2, 3," ; "12, 1, 2"
        case _ if re.fullmatch(r"^(\d+,\s*)+\d+(?:,|\b)$", entry):
            # remove any trailing commas if present
            entry = entry.removesuffix(",")

            # split `entry` with "," and not ", " which is the value of `COMMA_DELIM`
            choices_str: list[str] = entry.split(COMMA_DELIM.strip())

            # strip any sequence of characters in `choices_str` with trailing or leading whitespaces
            choices_str = [char_seq.strip() for char_seq in choices_str]

            # perform match_date_by_index on each string of choices_str after converting to int
            choices_int: list[int] = [int(num_char) for num_char in choices_str]
            choices_int = list(set(choices_int))  # remove duplicates
            choices_int.sort()  # sort the list
            return Result.ok(choices_int)

        case _ if (
            re.fullmatch(
                r"^\s*((\d+\s*-\s*\d+\s*)|(\d+\s*))((,\s*\d+\s*-\s*\d+\s*)|(,\s*\d+\s*))*(?:,|\b)$",
                entry,
            )
            is not None
        ):
            entry = entry.strip()
            entries = entry.split(COMMA)
            entries = [entry.strip() for entry in entries]
            values: list[int] = []
            for entry in entries:
                match str(entry):
                    # matches "1", "12", "13", etc.,
                    case _ if re.fullmatch(r"^\s*\d+\s*$", entry) is not None:
                        entry = entry.strip()
                        entries = entry.split(COMMA)
                        entries = [entry.strip() for entry in entries]
                        new_values: list[int] = [int(entry) for entry in entries]
                        values.extend(new_values)
                    # matches "1-5", "1, 2-5"
                    case _ if re.fullmatch(r"^\s*(\d+\s*-\s*\d+)$", entry) is not None:
                        entry = entry.strip()
                        entries = entry.split(HYPHEN)
                        entries = [entry.strip() for entry in entries]
                        start = int(entries[0])
                        end = int(entries[1])
                        # error if start is greater than or equal to end
                        if start >= end:
                            msg = f"input {entry} does not match any of the required formats because its start is greater than or equal to the end"
                            eprint(msg)
                            return Result.err(msg)
                        values.extend(list(range(start, end + 1)))
                    # no match
                    case _:
                        msg = (
                            f"input {entry} does not match any of the required formats"
                        )
                        eprint(msg)
                        return Result.err(msg)

            # remove duplicates and sort the values
            set_of_values: set[int] = set(values)
            values = list(set_of_values)
            values.sort()
            return Result.ok(values)
        case _:
            return Result.ok([])
