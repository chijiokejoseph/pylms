from pylms.utils import DataStore, must_get_env
from pylms.cli import input_str
from pylms.messages.construct import construct_msg
from pylms.constants import NAME, GENDER, EMAIL
from email.message import EmailMessage
from pylms.messages.message_record import MessageRecord
from pylms.errors import Result


def build_all_message(ds: DataStore) -> Result[list[MessageRecord]]:
    """
    Build personalized email messages for each student in the DataStore.

    :param ds: (DataStore) - A DataStore object containing student data.
    :type ds: DataStore

    :return: (Result[list[MessageRecord]]) - A Result object containing a list of MessageRecord objects representing the personalized email messages.
    :rtype: Result[list[MessageRecord]]
    """
    # Get the number of rows (students) in the DataStore
    nrows: int = ds.as_ref().shape[0]

    # Initialize a list to collect any mail errors
    messages: list[MessageRecord] = []

    # Prompt user for the email subject title
    title: str = input_str("Enter the title of the message: ", lower_case=False)

    # Construct the email body; instructions included to avoid valedictions
    body: str = construct_msg(
        "Please do not enter any valedictions such as 'Yours Faithfully' or 'Best Regards'. This will be added automatically."
    )

    # Retrieve sender email from environment variables
    sender: str = must_get_env("EMAIL")

    # Iterate over each student to send personalized email
    for i in range(nrows):
        # Determine designation based on gender
        gender: str = ds.as_ref()[GENDER].astype(str).iloc[i]
        designation: str = (
            "Mr. "
            if gender.startswith("M")
            else "Ms. "
            if gender.startswith("F")
            else ""
        )

        # Retrieve student name and email
        name: str = ds.as_ref()[NAME].astype(str).iloc[i]
        email: str = ds.as_ref()[EMAIL].astype(str).iloc[i]

        # Create an EmailMessage object and set its subject
        message: EmailMessage = EmailMessage()
        message["Subject"] = title
        message["From"] = sender

        # Construct the HTML body of the email
        html_body: str = f"""
<h2 style="padding-bottom: 4px; font-size: 18px; font-weight: bold">
    Dear {designation}{name}
</h2>
<br>
<p style="text-transform: uppercase; padding-bottom: 4px; font-weight: bold; text-align: center;">{title}</p>
{"\n".join([f"<p style='padding-bottom: 1px'>{line}</p>" for line in body.split("\n")])}
<br>
<footer style="padding: 4px">
    <p style="font-weight: bold">Best Regards</p>
    <p style="font-weight: bold; font-style: italic">Jason, Joseph and King</p>
</footer>
        """
        message.set_content(html_body, subtype="html")
        messages.append(MessageRecord(name=name, email=email, message=message))
    return Result[list[MessageRecord]].ok(messages)


def build_assessment_message(ds: DataStore) -> list[MessageRecord]:
    return []


