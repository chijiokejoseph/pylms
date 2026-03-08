from ..cli_utils import verify_email, verify_gmail
from ..errors import Result
from ..info import print_info
from .custom_inputs import input_str


def input_email(
    msg: str,
    diagnosis: str | None = None,
    gmail: bool = True,
) -> Result[str]:
    """Prompt the user to enter and validate an email address.

    Args:
        msg: The prompt message shown to the user.
        diagnosis: Diagnosis message shown when validation fails.
        gmail: If True, validates Gmail addresses only. If False, validates any email format.

    Returns:
        Result[str]: Result.ok containing the validated email on success, or error Result on failure.
    """
    # Use Gmail validator if gmail=True, otherwise use general email validator
    validator = verify_gmail if gmail else verify_email

    if diagnosis is None:
        keyword = "gmail" if gmail else "email"
        diagnosis = f"Email entered is not a valid {keyword} address"
    
    result: Result[str] = input_str(msg, validator, diagnosis)
    if result.is_err():
        return result.propagate()
    
    chosen_email: str = result.unwrap()
    print_info(f"Email entered: {chosen_email} has been validated. You may proceed\n")
    return Result.ok(chosen_email)
