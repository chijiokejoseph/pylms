import re
from functools import partial
from typing import Callable

from ..constants import BACK_SLASH, COMMA, FRONT_SLASH, NA, SEMI, SPACE_DELIM
from ._clean_intl import (
    clean_intl,
    clean_intl_comma_sep,
    clean_intl_semi_sep,
    clean_intl_space_sep,
    clean_intl_special,
)
from ._clean_intl_irregular import (
    clean_intl_comp_irregular,
    clean_intl_irregular,
)
from ._clean_irregular import (
    clean_composite_irregular,
    clean_irregular_space,
)
from ._clean_local import (
    clean10,
    clean11,
    clean_comma_sep,
    clean_semi_sep,
    clean_space_sep,
)


def re_match(phone_str: str) -> Callable[[str], str]:
    match phone_str:
        case _ if re.fullmatch(r"^\d{10}$", phone_str):
            return clean10

        case _ if re.fullmatch(r"^0\d{10}$", phone_str):
            return clean11

        case _ if re.fullmatch(r"^(0\d{10}\s)+(0\d{10})\b$", phone_str):
            return clean_space_sep

        case _ if re.fullmatch(r"^(0\d{10},\s*)+(0\d{10})\b$", phone_str):
            return clean_comma_sep

        case _ if re.fullmatch(r"^(0\d{10};\s*)+(0\d{10})\b$", phone_str):
            return clean_semi_sep

        case _ if re.fullmatch(r"^0(?:\s*\d){10}$", phone_str):
            return clean_irregular_space

        case _ if re.fullmatch(r"^(0(?:\s*\d){10}\s)+(0(?:\s*\d){10})\b$", phone_str):
            return partial(clean_composite_irregular, delim=SPACE_DELIM)

        case _ if re.fullmatch(r"^(0(?:\s*\d){10},\s*)+(0(?:\s*\d){10})\b$", phone_str):
            return partial(clean_composite_irregular, delim=COMMA)

        case _ if re.fullmatch(r"^(0(?:\s*\d){10};\s*)+(0(?:\s*\d){10})\b$", phone_str):
            return partial(clean_composite_irregular, delim=SEMI)

        case _ if re.fullmatch(r"^(0(?:\s*\d){10}/\s*)+(0(?:\s*\d){10})\b$", phone_str):
            return partial(clean_composite_irregular, delim=FRONT_SLASH)

        case _ if re.fullmatch(
            r"^(0(?:\s*\d){10}\\\s*)+(0(?:\s*\d){10})\b$", phone_str
        ):
            return partial(clean_composite_irregular, delim=BACK_SLASH)

        case _ if re.fullmatch(r"^(\+\d+\d{10})\b$", phone_str):
            return clean_intl

        case _ if re.fullmatch(r"^(\+\d+\d{10}\s)+(\+\d+\d{10})\b$", phone_str):
            return clean_intl_space_sep

        case _ if re.fullmatch(r"^(\+\d+\d{10},\s*)+(\+\d+\d{10})\b$", phone_str):
            return clean_intl_comma_sep

        case _ if re.fullmatch(r"^(\+\d+\d{10};\s*)+(\+\d+\d{10})\b$", phone_str):
            return clean_intl_semi_sep

        case _ if re.fullmatch(r"^\+(?:\s*\d)+(?:\s*\d){10}$", phone_str):
            return clean_intl_irregular

        case _ if re.fullmatch(
            r"^(\+(?:\s*\d)+(?:\s*\d){10}\s)+(\+(?:\s*\d)+(?:\s*\d){10})\b$", phone_str
        ):
            return partial(clean_intl_comp_irregular, delim=SPACE_DELIM)

        case _ if re.fullmatch(
            r"^(\+(?:\s*\d)+(?:\s*\d){10},\s*)+(\+(?:\s*\d)+(?:\s*\d){10})\b$",
            phone_str,
        ):
            return partial(clean_intl_comp_irregular, delim=COMMA)

        case _ if re.fullmatch(
            r"^(\+(?:\s*\d)+(?:\s*\d){10};\s*)+(\+(?:\s*\d)+(?:\s*\d){10})\b$",
            phone_str,
        ):
            return partial(clean_intl_comp_irregular, delim=SEMI)

        case _ if re.fullmatch(r"^\d+\d{10}$", phone_str):
            return clean_intl_special

        case _:
            return lambda x: NA
