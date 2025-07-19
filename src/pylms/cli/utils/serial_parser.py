
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
    # match str(entry):
    #     case _ if re.fullmatch(r"^\s*\d+\s*$", entry) is not None:
    #         entry = entry.strip()
    #         return [int(entry)]

    #     case _ if re.fullmatch(r"^\s*(\d+\s*,\s*)+\d+(?:,|\b)$", entry) is not None:
    #         entry = entry.strip()
    #         choices: list[str] = entry.split(COMMA)
    #         choices = [choice.strip() for choice in choices]
    #         return [int(choice) for choice in choices]

    #     case _ if re.fullmatch(r"^\s*(\d+\s+)+\s*$", entry) is not None:
    #         entry = entry.strip()
    #         choices = entry.split(SPACE_DELIM)
    #         choices = [choice.strip() for choice in choices]
    #         return [int(choice) for choice in choices]

    #     case _ if re.fullmatch(r"^\s*\d+\s*-\s*\d+\b$", entry) is not None:
    #         entry = entry.strip()
    #         entries: list[str] = entry.split(HYPHEN)
    #         entries = [entry.strip() for entry in entries]
    #         start: int = int(entries[0])
    #         end: int = int(entries[1])
    #         if start >= end:
    #             raise InvalidSelectionInputError(
    #                 f"input {entry} does not match any of the required formats because its start is greater than or equal to the end"
    #             )
    #         return list(range(start, end + 1))

    #     case _ if re.fullmatch(
    #         r"^\s*((\d+\s*-\s*\d+\s*)|(\d+\s*))((,\s*\d+\s*-\s*\d+\s*)|(,\s*\d+\s*))*(?:,|\b)$",
    #         entry,
    #     ) is not None:
    #         entry = entry.strip()
    #         entries = entry.split(COMMA)
    #         entries = [entry.strip() for entry in entries]
    #         values: list[int] = []
    #         for entry in entries:
    #             match str(entry):
    #                 case _ if re.fullmatch(r"^\s*\d+\s*$", entry) is not None:
    #                     entry = entry.strip()
    #                     entries = entry.split(COMMA)
    #                     entries = [entry.strip() for entry in entries]
    #                     new_values: list[int] = [int(entry) for entry in entries]
    #                     values.extend(new_values)
    #                 case _ if re.fullmatch(r"^\s*(\d+\s*-\s*\d+)$", entry) is not None:
    #                     entry = entry.strip()
    #                     entries = entry.split(HYPHEN)
    #                     entries = [entry.strip() for entry in entries]
    #                     start = int(entries[0])
    #                     end = int(entries[1])
    #                     if start >= end:
    #                         raise InvalidSelectionInputError(
    #                             f"input {entry} does not match any of the required formats because its start is greater than or equal to the end"
    #                         )
    #                     values.extend(list(range(start, end + 1)))
    #                 case _:
    #                     raise InvalidSelectionInputError(
    #                         f"input {entry} does not match any of the required formats"
    #                     )
    #         values_set: set[int] = set(values)
    #         values = list(values_set)
    #         values.sort()
    #         return values

    #     case _:
    #         raise InvalidSelectionInputError(
    #             f"input {entry} does not match any of the required formats"
    #         )
