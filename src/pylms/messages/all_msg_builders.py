from pylms.cli.custom_inputs import input_str
from pylms.cli.option_input import input_option
from pylms.errors import Result
from pylms.history.history import History
from pylms.messages.construct import construct_msg
from pylms.messages.utils import TextBody


# Define a builder function to create the list of messages to send
def build_custom_all_msg() -> Result[TextBody]:
    """
    custom builder function that returns the text of a string

    :return: (str) - The main text a message is to hold
    :rtype: str
    """

    # Prompt user for the email subject title
    title_result = input_str("Enter the title of the message: ", lower_case=False)
    if title_result.is_err():
        return Result[TextBody].err(title_result.unwrap_err())
    title: str = title_result.unwrap()

    body_result = construct_msg(
        "Please do not enter any valedictions such as 'Yours Faithfully' or 'Best Regards'. This will be added automatically."
    )
    if body_result.is_err():
        return Result[TextBody].err(body_result.unwrap_err())
    body: str = body_result.unwrap()

    return Result[TextBody].ok(TextBody(title, body))


def build_assessment_all_msg(history: History) -> Result[TextBody]:
    options: list[str] = [
        "Midterm Assessment",
        "Final Assessment",
    ]

    # Check if the cohort attribute in history is None and return an error if so
    if history.cohort is None:
        msg: str = "history.cohort is None. Expected an int value."
        print(f"\n{msg}\n")
        return Result[TextBody].err(ValueError(msg))

    # Extract the cohort number from the history object
    cohort: int = history.cohort

    option_result = input_option(options, prompt="Select the assessment type")
    if option_result.is_err():
        return Result[TextBody].err(option_result.unwrap_err())
    pos, assessment_type = option_result.unwrap()
    id_result = input_str("Enter the Assessment ID: ", lower_case=False)
    if id_result.is_err():
        return Result[TextBody].err(id_result.unwrap_err())
    assessment_id: str = id_result.unwrap()

    # Define the email title using the cohort number
    title: str = f"Python Beginners Cohort {cohort} {assessment_type} {assessment_id}"

    print(f"\nForm title is {title}\n")

    url_result = input_str("Enter the form url: ", lower_case=False)
    if url_result.is_err():
        return Result[TextBody].err(url_result.unwrap_err())
    url: str = url_result.unwrap()

    body = f"""
Your {assessment_type} with ID: {assessment_id} for the Python Beginners Class for Cohort {cohort} has been scheduled. Please access the form at the scheduled time through the url provided in the link below.
<br>
FORM: {url}
    """

    return Result[TextBody].ok(TextBody(title, body))
