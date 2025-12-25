import re


def verify_class(entry: str) -> bool:
    """Validate a user's date-selection input string.

    Accepts several input forms commonly used to select class dates:
    - a single 1- or 2-digit index (e.g. "1")
    - a comma-separated list of indices (e.g. "1, 2")
    - a single date in "dd/mm/yyyy" form
    - a comma-separated list of dates in "dd/mm/yyyy" form
    - ranges of indices (e.g. "1-5")
    - the token "all"
    The function returns True when `entry` matches one of the accepted formats.

    Args:
        entry (str): The input string to validate.

    Returns:
        bool: True if `entry` matches an accepted date-selection format,
            False otherwise.
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
        case _ if (
            re.fullmatch(
                r"^\s*((\d+\s*-\s*\d+\s*)|(\d+\s*))((,\s*\d+\s*-\s*\d+\s*)|(,\s*\d+\s*))*(?:,|\b)$",
                entry,
            )
            is not None
        ):
            return True
        # matches valid date input "all"
        case "all":
            return True
        # no match
        case _:
            return False
