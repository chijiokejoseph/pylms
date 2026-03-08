import re


def verify_gmail(gmail: str) -> bool:
    """Validate a Gmail address.

    Checks whether the provided string is a valid Gmail address according to
    Gmail-specific validation: it must match the pattern
    r"^[a-zA-Z.\\d]+@gmail\\.com$" and must not be composed solely of digits
    before the @ sign.

    Args:
        gmail (str): The Gmail address to validate.

    Returns:
        bool: True if gmail is a valid Gmail address, False otherwise.
    """
    positive_test: re.Match[str] | None = re.fullmatch(
        r"[a-zA-Z.\d]+@gmail\.com", gmail
    )
    negative_test: re.Match[str] | None = re.fullmatch(r"\d+@gmail\.com", gmail)
    if positive_test is None or negative_test is not None:
        return False
    return True
