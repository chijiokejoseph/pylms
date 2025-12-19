import re


def validate_email(email_text: str) -> bool:
    """
    validates that the entered email passed as an argument to `email_text` is a valid gmail address.

    :param email_text: (str) - the entered email address to validate
    :type email_text: str

    :returns: True if `email_text` is validated as a gmail address
    :rtype: bool
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
