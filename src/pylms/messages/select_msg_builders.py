from pylms.messages.message_record import MessageRecord
from pylms.cli import input_str
from pylms.models.form_info import CDSFormInfo, UpdateFormInfo
from pylms.utils import must_get_env
from pylms.messages.construct import construct_msg
from email.message import EmailMessage
from pylms.forms import select_form
from pylms.errors import Result
from pylms.history import History
from pylms.messages.utils import provide_emails


def build_select_message() -> Result[list[MessageRecord]]:
    """
    Build a list of MessageRecord objects for sending a select message to multiple recipients.

    :return: (Result[list[MessageRecord]]) - A Result object containing a list of MessageRecord objects if successful,
             or an error if the cohort is None.
    :rtype: Result[list[MessageRecord]]
    """
    # Prompt for the title of the message for each recipient
    title: str = input_str("Enter the title of the message: ", lower_case=False)
    
    # Construct the message body to be included in each email
    msg_body: str = construct_msg("Enter the message to be included in each email")

    # Retrieve the list of email addresses to send the message to
    emails: list[str] = provide_emails()

    # Initialize an empty list to hold the MessageRecord objects
    messages: list[MessageRecord] = []

    # Retrieve the sender's email address from environment variables
    sender: str = must_get_env("EMAIL")
    
    # Construct the HTML body of the email with styling and content
    body = f"""
<h2 style="padding-bottom: 8px; font-size: 18px; font-weight: bold">Dear Intern</h2>
<br>
<p style=""text-transform: uppercase; padding-bottom: 4px; font-weight: bold; text-align: center">{title}</p>
<p>{"\n".join([f"<p style='padding-bottom: 1px'>{line}</p>" for line in msg_body.split("\n")])}</p>
<br>
<footer style="padding: 4px;">
    <p style="padding-bottom: 1px; font-weight: bold">Best Regards</p>
    <p style="padding-bottom: 1px; font-weight: bold; font-style: italic">Jason, Joseph and King</p>
</footer>
        """
    
    # Create the email message object
    message: EmailMessage = EmailMessage()
    # Set the email subject to the title provided
    message["Subject"] = title
    # Set the sender's email address
    message["From"] = sender
    # Set the email content as HTML
    message.set_content(body, subtype="html")

    # Iterate over each email address to send the message
    for email in emails:
        # Append the constructed MessageRecord to the messages list
        messages.append(MessageRecord(name=None, email=email, message=message))

    # Return the list of MessageRecord objects
    return Result[list[MessageRecord]].ok(messages)


def build_update_form_msg(history: History) -> Result[list[MessageRecord]]:
    """
    Build a list of MessageRecord objects for sending an update form message based on the provided history.

    :param history: (History) - The history object containing cohort information.
    :type history: History

    :return: (Result[list[MessageRecord]]) - A Result object containing a list of MessageRecord objects if successful,
             or an error if the cohort is None.
    :rtype: Result[list[MessageRecord]]
    """
    # Retrieve the URL for the update form from the history object
    result: Result[CDSFormInfo | UpdateFormInfo] = select_form(history, "update")
    if result.is_err():
        return Result[list[MessageRecord]].err(result.unwrap_err())
    
    url: str = result.unwrap().url

    # Check if the cohort attribute in history is None and return an error if so
    if history.cohort is None:
        return Result[list[MessageRecord]].err(ValueError("history.cohort is None. Expected an int value."))

    # Extract the cohort number from the history object
    cohort: int = history.cohort

    # Define the email title using the cohort number
    title: str = f"Python Beginners Cohort {cohort} Onboarding"

    # Initialize an empty list to hold the MessageRecord objects
    messages: list[MessageRecord] = []

    # Retrieve the list of email addresses to send the message to
    emails: list[str] = provide_emails()

    # Construct the HTML body of the email with styling and content
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
    # Retrieve the sender's email address from environment variables
    sender: str = must_get_env("EMAIL")

    # Create the email message object
    message: EmailMessage = EmailMessage()
    # Set the email subject to the title
    message["Subject"] = title
    # Set the sender's email address
    message["From"] = sender
    # Set the email content as HTML
    message.set_content(body, subtype="html")

    # Iterate over each email address and create a MessageRecord for each
    for email in emails:
        messages.append(MessageRecord(name=None, email=email, message=message))

    # Return a successful Result containing the list of MessageRecord objects
    return Result[list[MessageRecord]].ok(messages)
