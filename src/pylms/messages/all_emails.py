from email.message import EmailMessage
from smtplib import SMTP

from ..constants import COMMA_DELIM, EMAIL, GENDER, NAME, SPACE_DELIM
from ..data import DataStore
from ..email import MailError, run_email
from ..errors import Result, Unit
from ..history import History
from ..paths import must_get_env
from .all_msg_builders import (
    build_assessment_all_msg,
    build_custom_all_msg,
)
from .message_record import MessageRecord
from .utils import MessageBuilder, TextBody


def _construct_html_message(
    *, title: str, designation: str, name: str, body: str
) -> str:
    return f"""
<h2 style="padding-bottom: 4px; font-size: 18px; font-weight: bold">
    Dear {designation}{name}
</h2>
<br>
<p style="text-transform: uppercase; padding-bottom: 4px; font-weight: bold; text-align: center;">{title}</p>
{"\n".join([f"<p style='padding-bottom: 1px'>{line}</p>" for line in body.split("\n")])}
<br>
<footer style="padding: 4px">
    <p style="font-weight: bold">Best Regards</p>
    <p style="font-weight: bold; font-style: italic">Jason, Joseph</p>
</footer>
        """


def _build_all_message(
    ds: DataStore, builder: MessageBuilder
) -> Result[list[MessageRecord]]:
    """
    Build personalized email messages for each student in the DataStore.

    :param ds: (DataStore) - A DataStore object containing student data.
    :type ds: DataStore

    :param builder: (MessageBuilder) - A builder to return the text body to be used in the email message.
    :type body: MessageBuilder

    :return: (Result[list[MessageRecord]]) - A Result object containing a list of MessageRecord objects representing the personalized email messages.
    :rtype: Result[list[MessageRecord]]
    """
    # Get the number of rows (students) in the DataStore
    nrows: int = ds.as_ref().shape[0]

    # Initialize a list to collect any mail errors
    messages: list[MessageRecord] = []

    # Retrieve sender email from environment variables
    sender: str = must_get_env("EMAIL")

    result: Result[TextBody] = builder()
    if result.is_err():
        return result.propagate()

    title, body = result.unwrap()

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
        name: str = (
            ds.as_ref()[NAME].astype(str).iloc[i].replace(COMMA_DELIM, SPACE_DELIM)
        )
        email: str = ds.as_ref()[EMAIL].astype(str).iloc[i]

        # Create an EmailMessage object and set its subject
        message: EmailMessage = EmailMessage()
        message["Subject"] = title
        message["From"] = sender

        # construct the html email message from its parameters
        html_body = _construct_html_message(
            title=title, designation=designation, name=name, body=body
        )
        message.set_content(html_body, subtype="html")
        messages.append(MessageRecord(name=name, email=email, message=message))
    return Result.ok(messages)


def _message_all_emails(
    server: SMTP, ds: DataStore, builder: MessageBuilder
) -> Result[Unit]:
    """
    Send personalized emails to all students using the provided SMTP server.

    :param server: (SMTP) - An SMTP server instance used to send emails.
    :type server: SMTP

    :param builder: (MessageBuilder) - A callable that returns a result
                    object containing the email title and body.
    :type builder: MessageBuilder


    :return: (Result[Unit]) - returns a Result object indicating success or failure.
    :rtype: Result[Unit]
    """

    # Initialize a list to collect any mail errors
    errors: list[MailError] = []

    # Retrieve sender email from environment variables
    sender: str = must_get_env("EMAIL")

    # Call the builder function to get the list of messages to send
    result: Result[list[MessageRecord]] = _build_all_message(ds, builder)
    if result.is_err():
        # Return error result if builder failed
        return result.propagate()

    # Unwrap the result to get the list of MessageRecord objects
    messages: list[MessageRecord] = result.unwrap()

    # Iterate over each message and send it
    for i, message in enumerate(messages):
        name: str | None = message.name
        content: EmailMessage = message.message
        email: str = message.email
        try:
            # Attempt to send the email via the SMTP server
            err: MailError = server.send_message(
                content, from_addr=sender, to_addrs=email
            )
            # Check if there were any errors sending to this email
            if err != {}:
                # Append any errors to the errors list
                errors.append({f"{i + 1}": (1, bytes(str(err), "utf-8"))})
                continue
            print(
                f"\nMail sent successfully to {f'{name} with ' if name is not None else ''}{email}\n"
            )
        except Exception as e:
            # Catch any exceptions during sending and record the error
            errors.append({f"{i + 1}": (1, bytes(str(e), "utf-8"))})
            continue

    # If there were any errors, print detailed error messages
    if len(errors) > 0:
        for err in errors:
            for index in err:
                # Extract the name, and email for which sending failed
                i = int(index)
                err_name: str | None = messages[i - 1].name
                err_email: str = messages[i - 1].email
                # Craft a detailed error message
                if err_name is None:
                    err_print: str = f"{i}. Failed to send email to {err_email}"
                else:
                    err_print = f"{i}. Failed to send email to {err_name} with email: {err_email}"
                # Print the error message with recipient name and email address
                print(err_print)
            print()
        # Return an error result if there were failures
        return result.propagate()

    # Return a success result if all emails were sent
    return Result.unit()


def custom_message_all(ds: DataStore) -> Result[Unit]:
    """
    Send a message to all email addresses stored in the provided DataStore.

    This function initiates the process of sending a message to all recipients listed in the DataStore.
    It delegates the actual email sending to a helper function, which is executed within
    a managed SMTP session provided by `run_email`. The function ensures that the SMTP connection is
    properly established and closed, and that any errors encountered during the email sending process
    are captured and returned as part of the Result object.

    :param ds: (DataStore) - The data source containing recipient information
    (must include columns for gender, name, and email).
    :type ds: DataStore

    :return: (Result[Unit]) - Returns a Result object indicating success or failure
    of the email sending operation.
    :rtype: Result[Unit]
    """

    # Use run_email to establish SMTP connection and execute the email sending routine
    return run_email(
        lambda service: _message_all_emails(
            service,
            ds,
            build_custom_all_msg,
        )
    )


def assessment_message_all(ds: DataStore, history: History) -> Result[Unit]:
    def _builder_intermediary() -> Result[TextBody]:
        return build_assessment_all_msg(history)

    return run_email(
        lambda service: _message_all_emails(service, ds, _builder_intermediary)
    )
