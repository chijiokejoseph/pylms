from ..cli_utils import verify_email
from ..errors import Result
from ..info import print_info
from .custom_inputs import input_str


def input_email(
    msg: str, diagnosis: str = "Email entered is not a valid email address"
) -> Result[str]:
    """Prompt the user to enter and validate an email address.

    This function wraps `input_str` supplying the `validate_email` validator to
    prompt the user for an email address (a Gmail address is expected by the
    validator). If the user input validates, the validated email is returned
    inside `Result.ok`. If the interactive prompt returns an error, that
    error `Result` is propagated.

    Args:
        msg (str): The prompt message shown to the user.
        diagnosis (str): Optional diagnosis message shown when validation
            fails. Defaults to "Email entered is not a valid email address".

    Returns:
        Result[str]: `Result.ok` containing the validated email on success, or
            an error `Result` propagated from the input helper on failure.
    """
    result: Result[str] = input_str(msg, verify_email, diagnosis)
    if result.is_err():
        return result.propagate()
    chosen_email: str = result.unwrap()
    print_info(f"Email entered: {chosen_email} has been validated. You may proceed\n")
    return Result.ok(chosen_email)
