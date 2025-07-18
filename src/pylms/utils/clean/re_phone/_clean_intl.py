from pylms.constants import SEMI_DELIM, SPACE_DELIM, COMMA_DELIM


def _clean_intl(entry: str) -> str:
    # extract the normal 10-digits of the intl phone number
    digits: str = entry[-10::]
    len_rem: int = len(entry) - len(digits)
    # extract the unique intl part of the intl phone number
    intl_id: str = entry[1:len_rem]
    # return the string formatted as e.g., "+234 80555423344;"
    return f"+{intl_id} {digits}{SEMI_DELIM}".strip()


def _clean_intl_special(entry: str) -> str:
    # extract the normal 10-digits of the intl phone number
    digits: str = entry[-10::]
    len_rem: int = len(entry) - len(digits)
    # extract the unique intl part of the intl phone number
    intl_id: str = entry[:len_rem]
    # return the string formatted as e.g., "+234 80555423344;"
    return f"+{intl_id} {digits}{SEMI_DELIM}".strip()


def _clean_intl_composite(entry: str, delim: str) -> str:
    entries: list[str] = entry.split(delim)
    output: str = ""
    for each_entry in entries:
        each_entry = each_entry.strip()
        output += _clean_intl(each_entry) + SPACE_DELIM
    return output.strip()


def _clean_intl_space_sep(entry: str) -> str:
    return _clean_intl_composite(entry, SPACE_DELIM)


def _clean_intl_comma_sep(entry: str) -> str:
    return _clean_intl_composite(entry, COMMA_DELIM.strip())


def _clean_intl_semi_sep(entry: str) -> str:
    return _clean_intl_composite(entry, SEMI_DELIM.strip())
