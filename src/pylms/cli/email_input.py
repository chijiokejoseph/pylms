from pylms.cli.custom_inputs import input_str
from pylms.cli.utils import validate_email


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
