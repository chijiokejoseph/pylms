import re


def validate_email(email_text: str) -> bool:
    """Validate a Gmail address.

    Checks whether the provided string is a valid Gmail address according to a
    simple project validation: it must match the pattern
    r'^[a-zA-Z.\d]+@gmail\.com$' and must not be composed solely of digits
    before the @ sign.

    Args:
        email_text (str): The email address to validate.

    Returns:
        bool: True if `email_text` is a valid Gmail address, False otherwise.
    """

    # this tests that the email contains a combination of letters and numbers
    # before the signature `@gmail.com` e.g., email_text = "abc2@gmail.com"
    positive_test: re.Match[str] | None = re.fullmatch(
        r"^[a-zA-Z.\d]+@gmail\.com$", email_text
    )

    # this tests that the email does not contain only numbers
    # before the signature `@gmail.com` e.g., email_text = "11112223@gmail.com" ❌
    negative_test: re.Match[str] | None = re.fullmatch(r"^\d+@gmail\.com$", email_text)
    if positive_test is None or negative_test is not None:
        return False
    return True
