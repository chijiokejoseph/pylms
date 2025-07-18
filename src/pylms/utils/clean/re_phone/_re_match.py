import re
from functools import partial
from typing import Callable

from pylms.constants import BACK_SLASH, COMMA, FRONT_SLASH, NA, SEMI, SPACE_DELIM
from pylms.utils.clean.re_phone._clean_intl import (
    _clean_intl,
    _clean_intl_comma_sep,
    _clean_intl_semi_sep,
    _clean_intl_space_sep,
    _clean_intl_special,
)
from pylms.utils.clean.re_phone._clean_intl_irregular import (
    _clean_intl_comp_irregular,
    _clean_intl_irregular,
)
from pylms.utils.clean.re_phone._clean_irregular import (
    _clean_composite_irregular,
    _clean_irregular_space,
)
from pylms.utils.clean.re_phone._clean_local import (
    _clean10,
    _clean11,
    _clean_comma_sep,
    _clean_semi_sep,
    _clean_space_sep,
)


def _re_match(phone_str: str) -> Callable[[str], str]:
    match phone_str:
        case _ if re.fullmatch(r"^\d{10}$", phone_str):
            return _clean10

        case _ if re.fullmatch(r"^0\d{10}$", phone_str):
            return _clean11

        case _ if re.fullmatch(r"^(0\d{10}\s)+(0\d{10})\b$", phone_str):
            return _clean_space_sep

        case _ if re.fullmatch(r"^(0\d{10},\s*)+(0\d{10})\b$", phone_str):
            return _clean_comma_sep

        case _ if re.fullmatch(r"^(0\d{10};\s*)+(0\d{10})\b$", phone_str):
            return _clean_semi_sep

        case _ if re.fullmatch(r"^0(?:\s*\d){10}$", phone_str):
            return _clean_irregular_space

        case _ if re.fullmatch(r"^(0(?:\s*\d){10}\s)+(0(?:\s*\d){10})\b$", phone_str):
            return partial(_clean_composite_irregular, delim=SPACE_DELIM)

        case _ if re.fullmatch(r"^(0(?:\s*\d){10},\s*)+(0(?:\s*\d){10})\b$", phone_str):
            return partial(_clean_composite_irregular, delim=COMMA)

        case _ if re.fullmatch(r"^(0(?:\s*\d){10};\s*)+(0(?:\s*\d){10})\b$", phone_str):
            return partial(_clean_composite_irregular, delim=SEMI)

        case _ if re.fullmatch(r"^(0(?:\s*\d){10}/\s*)+(0(?:\s*\d){10})\b$", phone_str):
            return partial(_clean_composite_irregular, delim=FRONT_SLASH)

        case _ if re.fullmatch(
            r"^(0(?:\s*\d){10}\\\s*)+(0(?:\s*\d){10})\b$", phone_str
        ):
            return partial(_clean_composite_irregular, delim=BACK_SLASH)

        case _ if re.fullmatch(r"^(\+\d+\d{10})\b$", phone_str):
            return _clean_intl

        case _ if re.fullmatch(r"^(\+\d+\d{10}\s)+(\+\d+\d{10})\b$", phone_str):
            return _clean_intl_space_sep

        case _ if re.fullmatch(r"^(\+\d+\d{10},\s*)+(\+\d+\d{10})\b$", phone_str):
            return _clean_intl_comma_sep

        case _ if re.fullmatch(r"^(\+\d+\d{10};\s*)+(\+\d+\d{10})\b$", phone_str):
            return _clean_intl_semi_sep

        case _ if re.fullmatch(r"^\+(?:\s*\d)+(?:\s*\d){10}$", phone_str):
            return _clean_intl_irregular

        case _ if re.fullmatch(
            r"^(\+(?:\s*\d)+(?:\s*\d){10}\s)+(\+(?:\s*\d)+(?:\s*\d){10})\b$", phone_str
        ):
            return partial(_clean_intl_comp_irregular, delim=SPACE_DELIM)

        case _ if re.fullmatch(
            r"^(\+(?:\s*\d)+(?:\s*\d){10},\s*)+(\+(?:\s*\d)+(?:\s*\d){10})\b$",
            phone_str,
        ):
            return partial(_clean_intl_comp_irregular, delim=COMMA)

        case _ if re.fullmatch(
            r"^(\+(?:\s*\d)+(?:\s*\d){10};\s*)+(\+(?:\s*\d)+(?:\s*\d){10})\b$",
            phone_str,
        ):
            return partial(_clean_intl_comp_irregular, delim=SEMI)

        case _ if re.fullmatch(r"^\d+\d{10}$", phone_str):
            return _clean_intl_special

        case _:
            return lambda x: NA
