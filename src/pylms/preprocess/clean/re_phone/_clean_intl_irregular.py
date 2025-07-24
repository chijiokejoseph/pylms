from pylms.constants import SPACE_DELIM
from pylms.preprocess.clean.re_phone._clean_intl import _clean_intl


def _clean_intl_irregular(entry: str) -> str:
    """
    formats an international phone number with spaces in between it and random by
        - replacing all its spaces with an emtpy string
        e.g., "+234 90 59 2871 84" -> "+2349059287184"
        - the obtained format is suitable for the formatting with the function for
        cleaning single international strings
        - hence the result is passed to `_clean_intl`

    :param entry: ( str ): The number to be formatted
    :type entry: str

    :rtype: str
    :return: formatted international number
    """
    entry = entry.replace(SPACE_DELIM, "")
    return _clean_intl(entry)


def _clean_intl_comp_irregular(entry: str, delim: str) -> str:
    # if the entry is not separated by spaces
    if delim != SPACE_DELIM:
        # split the entry into its distinct phone number strings
        entries: list[str] = entry.split(delim)

        output: str = ""

        # for each intl phone number string (which is basically an irregular),
        # format the intl phone number string using the func for irregulars
        # sum the numbers with a space between
        for each_entry in entries:
            output += _clean_intl_irregular(each_entry) + SPACE_DELIM

        # return a stripped version
        return output.strip()
    else:
        # create a string copy to track the formatting of the phone numbers.
        # This string copy is to have every whitespace in it removed.
        new_entry: str = entry.replace(SPACE_DELIM, "")

        output = ""

        # while the string copy still has a + found inside it,
        # i.e., still yet an international number that is yet to be formatted.
        while new_entry.find("+") != -1:
            # since + begins the very first phone number,
            # we track the next phone number by finding `+`
            # in the remaining part of the string i.e., `temp_str`
            temp_str: str = new_entry[1:]

            # get index of next `+` or starting point of next phone number
            next_plus_idx: int = temp_str.find("+")

            # get all chars from the start of `new_entry` to right before
            # the start of the next intl phone number
            each_entry = new_entry[:next_plus_idx]

            # each gotten entry is suitable for formatting by `_clean_intl_irregular`
            output += _clean_intl_irregular(each_entry) + SPACE_DELIM

            # the string copy is updated by removing the numbers that have been
            # formatted, allowing the operation to continue until new_entry is empty.
            new_entry = new_entry[next_plus_idx:]
        return output.strip()
