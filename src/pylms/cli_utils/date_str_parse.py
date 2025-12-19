import re

from ..constants import COMMA_DELIM


def parse_date_str(entry: str) -> list[str]:
    """
    Parse a date string or a comma-separated list of date strings into a list of date strings.

    :param entry: (str) - A date string or comma-separated date strings in the format dd/mm/yyyy.
    :type entry: str

    :return: (list[str]) - List of date strings parsed from the input.
    :rtype: list[str]
    """
    match str(entry):
        # matches a single date string like "12/11/2030" or "09/03/2004"
        case _ if re.fullmatch(r"^\d{2}/\d{2}/\d{4}$", entry):
            return [entry]

        # matches multiple date strings separated by commas, e.g. "12/11/2023, 01/05/1019"
        case _ if re.fullmatch(
            r"^(\d{2}/\d{2}/\d{4},\s)+\d{2}/\d{2}/\d{4}(?:,|\b)$", entry
        ):
            # Remove any trailing commas
            entry = entry.removesuffix(",")

            # Split the entry by commas (not including spaces)
            choices_str = entry.split(COMMA_DELIM.strip())

            # Strip whitespace from each date string
            choices_str = [char_seq.strip() for char_seq in choices_str]

            # Return the list of cleaned date strings
            return [choice_str for choice_str in choices_str]

        # If input does not match expected formats, return empty list
        case _:
            return []
