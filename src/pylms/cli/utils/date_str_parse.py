import re

from pylms.constants import COMMA_DELIM

def _parse_date_str(entry: str) -> list[str]:
    match str(entry):
        # matches "12/11/2030", "09/03/2004"
        case _ if re.fullmatch(r"^\d{2}/\d{2}/\d{4}$", entry):
            return [entry]

        # matches "12/11/2023, 01/05/1019"; "14/09/2007, 13/02/2014,"
        case _ if re.fullmatch(
            r"^(\d{2}/\d{2}/\d{4},\s)+\d{2}/\d{2}/\d{4}(?:,|\b)$", entry
        ):
            # remove any trailing commas if present.
            entry = entry.removesuffix(",")

            # split `entry` with "," and not ", " which is the value of `COMMA_DELIM`
            choices_str = entry.split(COMMA_DELIM.strip())

            # strip any sequence of characters in `choices_str` with trailing or leading whitespaces
            choices_str = [char_seq.strip() for char_seq in choices_str]

            # perform match_date_by_value on each string of choices_str
            return [choice_str for choice_str in choices_str]
        
        case _:
            return []
