from pylms.cli.custom_inputs import input_str
from pylms.messages.construct import construct_msg
from pylms.models.form_info import CDSFormInfo, UpdateFormInfo
from pylms.forms import select_form
from pylms.errors import Result
from pylms.history import History
from pylms.messages.utils import TextBody


def build_custom_select_msg() -> Result[TextBody]:
    """
    Build a list of MessageRecord objects for sending a select message to multiple recipients.

    :return: (Result[list[MessageRecord]]) - A Result object containing a list of MessageRecord objects if successful,
             or an error if the cohort is None.
    :rtype: Result[list[MessageRecord]]
    """

    # Prompt for the title of the message for each recipient
    title: str = input_str("Enter the title of the message: ", lower_case=False)

    body: str = construct_msg("Enter the message to be included in each email")

    html_body: str = f"""
<h2 style="padding-bottom: 8px; font-size: 18px; font-weight: bold">Dear Intern</h2>
<br>
<p style=""text-transform: uppercase; padding-bottom: 4px; font-weight: bold; text-align: center">{title}</p>
<p>{"\n".join([f"<p style='padding-bottom: 1px'>{line}</p>" for line in body.split("\n")])}</p>
<br>
<footer style="padding: 4px;">
    <p style="padding-bottom: 1px; font-weight: bold">Best Regards</p>
    <p style="padding-bottom: 1px; font-weight: bold; font-style: italic">Jason, Joseph and King</p>
</footer>
        """

    return Result[TextBody].ok(TextBody(title, html_body))


def build_update_msg(history: History) -> Result[TextBody]:
    # Retrieve the URL for the update form from the history object
    result: Result[CDSFormInfo | UpdateFormInfo] = select_form(history, "update")
    if result.is_err():
        return Result[TextBody].err(result.unwrap_err())

    url: str = result.unwrap().url

    # Check if the cohort attribute in history is None and return an error if so
    if history.cohort is None:
        return Result[TextBody].err(
            ValueError("history.cohort is None. Expected an int value.")
        )

    # Extract the cohort number from the history object
    cohort: int = history.cohort

    # Define the email title using the cohort number
    title: str = f"Python Beginners Cohort {cohort} Onboarding"

    body: str = f"""
<h2 style="padding: 8px; font-weight: bold;">
    Dear Intern
</h2>
<br>
<p style="text-align: center; text-transform: uppercase; font-weight: bold padding: 4px">{title}</p>
<p style="padding: 1px">Your registration for the Python Beginners Class for Cohort {cohort} has been confirmed. Please fill out the form attached below</p>
<br>
<p style="padding: 1px">FORM: {url}</p>
<br>
<footer style="padding: 1px">
    <p style="font-weight: bold; font-style: italic">Best Regards</p>
    <p style="font-weight: bold; font-style: italic">Jason, Joseph and King</p>
</footer>
    """

    return Result[TextBody].ok(TextBody(title, body))
