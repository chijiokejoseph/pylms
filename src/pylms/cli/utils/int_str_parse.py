import re
from pylms.constants import COMMA_DELIM, COMMA, HYPHEN
from pylms.cli.errors import InvalidSelectionInputError

# TODO: test this function
def _parse_int_str(entry: str) -> list[int]:
    """Parses a string containing integers and returns a list of integers.
    The string can contain integers separated by commas, spaces, or hyphens.
    :param entry: (str) - The input string to parse.
    :type entry: str

    :return: (list[int]) - A list of integers parsed from the input string.
    :rtype: list[int]

    :raises InvalidSelectionInputError: If the input string does not match any of the required formats.
    """

    match str(entry):
        # matches "1", "12", "13", etc.,
        case _ if re.fullmatch(r"^\d{1,2}$", entry):
            choice: int = int(entry)
            return [choice]

        # matches "1, 2, 3," ; "12, 1, 2"
        case _ if re.fullmatch(r"^(\d{1,2},\s*)+\d{1,2}(?:,|\b)$", entry):
            # remove any trailing commas if present
            entry = entry.removesuffix(",")

            # split `entry` with "," and not ", " which is the value of `COMMA_DELIM`
            choices_str: list[str] = entry.split(COMMA_DELIM.strip())

            # strip any sequence of characters in `choices_str` with trailing or leading whitespaces
            choices_str = [char_seq.strip() for char_seq in choices_str]

            # perform match_date_by_index on each string of choices_str after converting to int
            return [int(num_char) for num_char in choices_str]

        case _ if re.fullmatch(
            r"^\s*((\d+\s*-\s*\d+\s*)|(\d+\s*))((,\s*\d+\s*-\s*\d+\s*)|(,\s*\d+\s*))*(?:,|\b)$",
            entry,
        ) is not None:
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
                            raise InvalidSelectionInputError(
                                f"input {entry} does not match any of the required formats because its start is greater than or equal to the end"
                            )
                        values.extend(list(range(start, end + 1)))
                    # no match
                    case _:
                        raise InvalidSelectionInputError(
                            f"input {entry} does not match any of the required formats"
                        )
                        
            # remove duplicates and sort the values
            set_of_values: set[int] = set(values)
            values = list(set_of_values)
            values.sort()
            return values
        case _:
            return []
