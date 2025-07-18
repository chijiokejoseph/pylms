from pylms.constants import SEMI_DELIM, SPACE_DELIM, COMMA_DELIM


def _clean10(entry: str) -> str:
    """
    Formats a series of 10 valid digits by adding a leading '0' to the string and adding a trailing semicolon.
    The rationale behind this is the pandas handling of phone numbers. They are read as numbers instead of strings and their leading 0s are ignored as are done in positive numbers.
    By adding a leading '0' to the string and adding a trailing semicolon, pandas recognizes the phone number as a string and no longer tries to convert it to numbers.

    :param entry: ( str ): Local 10-digit phone number to be formatted
    :type entry: str

    :rtype: str
    :return: formatted local phone number
    """
    return f"0{entry}{SEMI_DELIM}".strip()


def _clean11(entry: str) -> str:
    """
    Formats an 11-digit string that already has a 0 as its leading character by adding a trailing semicolon to the string to force pandas to recognize it as a string and no longer try to convert it to a number.

    :param entry: ( str ): Local 11-digit phone number to be formatted
    :type entry: str

    :rtype: str
    :return: formatted local phone number
    """
    return f"{entry}{SEMI_DELIM}".strip()


def _clean_composite(entry: str, delim: str) -> str:
    """
     Generic function for formatting a concatenation of phone numbers which are separated by `delim`.

         - The phone numbers are split using `delim`,
         - Each single phone number is stripped and formatted using the `_clean11` function,
         - The results are concatenated
         - Then stripped again and returned.

    :param entry: ( str ): Concatenation of 11-digit phone numbers to be formatted
    :type entry: str
    :param delim: ( str ) : Delimiter or separator of phone numbers
    :type delim: str

    :rtype: str
    :return: formatted local phone number
    """
    entries: list[str] = entry.split(delim)
    output: str = ""
    for each_entry in entries:
        each_entry = each_entry.strip()
        output += _clean11(each_entry) + SPACE_DELIM
    return output.strip()


def _clean_space_sep(entry: str) -> str:
    """
    formats a concatenation of phone numbers separated by a space. Calls the `_clean_composite` function, with its `delim` argument set to `SPACE_DELIM`.

    :param entry: ( str ): Concatenation of 11-digit phone numbers to be formatted separated by a space
    :type entry: str

    :rtype: str
    :return: formatted local phone number
    """
    return _clean_composite(entry, SPACE_DELIM)


def _clean_comma_sep(entry: str) -> str:
    """
    formats a concatenation of phone numbers separated by a space. Calls the `_clean_composite` function, with its `delim` argument set to `COMMA_DELIM`.

    :param entry: ( str ): Concatenation of 11-digit phone numbers to be formatted separated by a comma
    :type entry: str

    :rtype: str
    :return: formatted local phone number
    """
    return _clean_composite(entry, COMMA_DELIM.strip())


def _clean_semi_sep(entry: str) -> str:
    """
    formats a concatenation of phone numbers separated by a space. Calls the `_clean_composite` function, with its `delim` argument set to `SEMI_DELIM`.

    :param entry: ( str ): Concatenation of 11-digit phone numbers to be formatted separated by a semicolon
    :type entry: str

    :rtype: str
    :return: formatted local phone number
    """
    return _clean_composite(entry, SEMI_DELIM.strip())
