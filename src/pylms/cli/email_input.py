import re

from pylms.cli.custom_inputs import input_str


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


def input_email(
    msg: str, diagnosis: str = "Email entered is not a valid email address"
) -> str:
    """
    prompts the user to enter an email (specifically a gmail) address using the `input_str` function. The `test_fn` argument is filled using a custom validation function defined in the same module called  `validate_email`.

    :param msg: (str) - the prompt to the user to enter an email (gmail) address
    :type msg: str
    :param diagnosis: (str, Optional) - the diagnosis text to display if the entered input by the user is not validated as a gmail address. Default to "Email entered is not a valid email address"
    :type diagnosis: str, optional

    :returns: input from the user if it is validated as a gmail address
    :rtype: str
    """
    chosen_email: str = input_str(msg, validate_email, diagnosis)
    print(f"Email entered: {chosen_email} has been validated. You may proceed\n")
    return chosen_email
