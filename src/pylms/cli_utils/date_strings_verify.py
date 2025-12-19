import re


def val_date_str(entry: str) -> bool:
    """Validate the date string format. The date string can be a single date,
    a comma-separated list of dates, or a range of dates.
    e.g., "1", "1, 2", "12/11/2023", "12/11/2023, 01/05/2024", "1-5", "1, 2-5".

    :param entry: (str) - The input string to validate.
    :type entry: str

    :return: (bool) - True if the input string matches the expected date formats, False otherwise.
    :rtype: bool

    :raises InvalidSelectionInputError: If the input string does not match any of the required formats.
    """

    # normalize the entry by stripping and lowercasing it
    entry = entry.strip().lower()
    match str(entry):
        # matches "1", "12", "13", etc.,
        case _ if re.fullmatch(r"^\d{1,2}$", entry):
            return True
        # matches "1, 2, 3," ; "12, 1, 2"
        case _ if re.fullmatch(r"^(\d{1,2},\s)+\d{1,2}(?:,|\b)$", entry):
            return True
        # matches "12/11/2023", "09/03/2004"
        case _ if re.fullmatch(r"^\d{2}/\d{2}/\d{4}$", entry):
            return True
        # matches "12/11/2023, 01/05/2024"; "14/09/2007, 13/02/2014,"
        case _ if re.fullmatch(
            r"^(\d{2}/\d{2}/\d{4},\s)+\d{2}/\d{2}/\d{4}(?:,|\b)$", entry
        ):
            return True
        # matches "1-5", "1, 2-5"
        case _ if re.fullmatch(
            r"^\s*((\d+\s*-\s*\d+\s*)|(\d+\s*))((,\s*\d+\s*-\s*\d+\s*)|(,\s*\d+\s*))*(?:,|\b)$",
            entry,
        ) is not None:
            return True
        # matches valid date input "all"
        case "all":
            return True
        # no match
        case _:
            return False
