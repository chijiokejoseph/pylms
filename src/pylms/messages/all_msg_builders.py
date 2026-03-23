from ..cli import input_option, input_str
from ..errors import Result
from ..history.history import History
from .construct import construct_msg
from .message import MessageBody


# Define a builder function to create the list of messages to send
def compose_custom_msg_body() -> Result[MessageBody]:
    """Build custom message content for all recipients.

    Prompts user for email title and message body content.

    Returns:
        Result[MessageBody]: Success with title and body or error.
    """

    # Prompt user for the email subject title
    result = input_str("Enter the title of the message: ", lower_case=False)
    if result.is_err():
        return result.propagate()
    title: str = result.unwrap()

    result = construct_msg(
        "Please do not enter any valedictions such as 'Yours Faithfully' or 'Best Regards'. This will be added automatically."
    )
    if result.is_err():
        return result.propagate()
    body: str = result.unwrap()

    return Result.ok(MessageBody(title, body))


def compose_assessment_msg_body(history: History) -> Result[MessageBody]:
    """Build assessment message content for all students.

    Args:
        history (History): History object containing cohort information.

    Returns:
        Result[MessageBody]: Success with assessment message or error.
    """
    options: list[str] = [
        "Midterm Assessment",
        "Final Assessment",
    ]

    # Check if the cohort attribute in history is None and return an error if so
    if history.cohort is None:
        msg: str = "history.cohort is None. Expected an int value."
        print(f"\n{msg}\n")
        return Result.err(ValueError(msg))

    # Extract the cohort number from the history object
    cohort: int = history.cohort

    result = input_option(options, prompt="Select the assessment type")
    if result.is_err():
        return result.propagate()
    _, assessment_type = result.unwrap()
    result = input_str("Enter the Assessment ID: ", lower_case=False)
    if result.is_err():
        return result.propagate()
    assessment_id: str = result.unwrap()

    # Define the email title using the cohort number
    title: str = f"Python Beginners Cohort {cohort} {assessment_type} {assessment_id}"

    print(f"\nForm title is {title}\n")

    result = input_str("Enter the form url: ", lower_case=False)
    if result.is_err():
        return result.propagate()
    url: str = result.unwrap()

    body = f"""
Your {assessment_type} with ID: {assessment_id} for the Python Beginners Class for Cohort {cohort} has been scheduled. Please access the form at the scheduled time through the url provided in the link below.
<br>
FORM: {url}
    """

    return Result.ok(MessageBody(title, body))
