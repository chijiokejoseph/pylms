import re


def val_date_str(entry: str) -> bool:
    """
    a private helper function that matches the argument passed to `entry` against several regular expressions after lowering and stripping the argument using the str methods .lower and .strip. the regular expressions attempt to match the `entry` argument against the following cases

        entry = entry.strip().lower()

        - case entry = "d" / "dd" e.g., "1" or "2" or "3" or "14" :

            only digit strings that contain only 1 or 2 digits are allowed
        - case entry = "d, d" / "d, dd" e.g., "1, 2, 3" or "12, 13, 2, 3" :

           only digits that are comma separated with no trailing or leading whitespaces or any other non-digit characters are allowed
           only digits that contain single digits or at most 2 digits adjacent to each other are allowed
        - case entry = "dd/mm/yyyy" e.g., "12/01/2025" or "13/01/2025":

            only string that match the form dd/mm/yyyy where every non-slash character is a digit is allowed.
        - case entry = "dd/mm/yyyy, dd/mm/yyyy, dd/mm/yyyy" e.g., "13/01/2025, 14/01/2025":

            only strings that are comma separated with no trailing or leading whitespaces or non-digit characters are allowed
            each collection of non-whitespace and non-comma characters must be of the form "dd/mm/yyyy"

    If the `entry` argument is matched, the function returns True else it returns False

    :param entry: (str): A string input passed in from the user
    :type entry: str

    :return: a True value if the `entry` argument is matched else False
    :rtype: bool
    """
    entry = entry.strip().lower()
    match str(entry):
        case _ if re.fullmatch(r"^\d{1,2}$", entry):
            return True
        case _ if re.fullmatch(r"^(\d{1,2},\s)+\d{1,2}(?:,|\b)$", entry):
            return True
        case _ if re.fullmatch(r"^\d{2}/\d{2}/\d{4}$", entry):
            return True
        case _ if re.fullmatch(
            r"^(\d{2}/\d{2}/\d{4},\s)+\d{2}/\d{2}/\d{4}(?:,|\b)$", entry
        ):
            return True
        case _ if re.fullmatch(
            r"^\s*((\d+\s*-\s*\d+\s*)|(\d+\s*))((,\s*\d+\s*-\s*\d+\s*)|(,\s*\d+\s*))*(?:,|\b)$",
            entry,
        ) is not None:
            return True
        case "all":
            return True
        case _:
            return False
