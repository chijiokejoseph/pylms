from email.message import EmailMessage
from smtplib import SMTP

from ..cli import provide_emails
from ..email import MailError, run_email
from ..errors import Result, Unit
from ..history import History
from ..info import print_info, printpass
from ..paths import must_get_env
from .message_record import MessageRecord
from .select_msg_builders import (
    build_custom_select_msg,
    build_update_msg,
)
from .utils import MessageBuilder, TextBody


def _build_select_message(builder: MessageBuilder) -> Result[list[MessageRecord]]:
    """
    Build a list of MessageRecord objects for sending a select message to multiple recipients.

    :return: (Result[list[MessageRecord]]) - A Result object containing a list of MessageRecord objects if successful,
             or an error if the cohort is None.
    :rtype: Result[list[MessageRecord]]
    """

    # Retrieve the list of email addresses to send the message to
    result: Result[list[str]] = provide_emails()
    if result.is_err():
        return result.propagate()
    emails: list[str] = result.unwrap()

    # Initialize an empty list to hold the MessageRecord objects
    messages: list[MessageRecord] = []

    # Retrieve the sender's email address from environment variables
    sender: str = must_get_env("EMAIL")

    # Construct the HTML body of the email with styling and content
    text_body_result: Result[TextBody] = builder()
    if text_body_result.is_err():
        return text_body_result.propagate()
    title, body = text_body_result.unwrap()

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
    return Result.ok(messages)


def message_select_emails(server: SMTP, builder: MessageBuilder) -> Result[Unit]:
    """
    Send emails to a list of recipients selected through various input formats.

    :param server: (SMTP) - The SMTP server instance used to send emails.
    :type server: SMTP

    :param builder: (Callable[[], Result[TextBody]) -
                    A function that returns a Result containing the TextBody object
                    that holds the title, and body of the message to be sent.
    :type builder: Callable[[], Result[TextBody]

    :return: (Result[Unit]) - Result indicating success or
                                failure of the email sending operation.
    :rtype: Result[Unit]

    This function prompts the user to select the format in which email addresses are provided,
    reads the email addresses from the selected format, constructs an email message for each recipient,
    and sends the emails using the provided SMTP server. It collects and reports any errors encountered
    during the sending process.
    """
    print("\nInitializing Sending Emails to provided emails...\n")

    errors: list[MailError] = []
    # retrieve the sender email from the environment
    sender: str = must_get_env("EMAIL")

    # get the messages to be sent by calling the passed in builder
    result = _build_select_message(builder)
    if result.is_err():
        # handle errors that occur during the building process
        return result.propagate()

    # get the list of messages to be sent
    messages: list[MessageRecord] = result.unwrap()

    # iterate over each message and send it
    for message in messages:
        name: str | None = message.name
        email: str = message.email
        content: EmailMessage = message.message
        try:
            # Attempt to send the email via the SMTP server
            err: dict[str, tuple[int, bytes]] = server.send_message(
                content, from_addr=sender, to_addrs=email
            )
            # Check if there were any errors sending to this email
            if err != {}:
                errors.append(
                    {email: (1, bytes(f"Failed to send email to {email}", "utf-8"))}
                )
                continue

            printpass(
                f"Mail sent successfully to {f'{name} with ' if name is not None else ''}{email}\n"
            )
        except Exception as e:
            print_info(
                f"Mail not sent to {f'{name} with ' if name is not None else ''}{email}\n"
            )
            # Catch any exceptions during sending and record the error
            errors.append(
                {
                    email: (
                        1,
                        bytes(f"Failed to send email to {email}. Error: {e}", "utf-8"),
                    )
                }
            )
            continue

    # If there were any errors, print detailed error messages
    if len(errors) > 0:
        for err in errors:
            for index in err:
                i = int(index)
                # Extract the recipient name and email address from the error
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
        return Result.err(ValueError("Failed to send emails"))

    # Return success result if all emails were sent without errors
    return Result.unit()


def custom_message_select() -> Result[Unit]:
    """
    Execute the email sending process by establishing an SMTP connection and running the email operation.
    The message to be sent is generated from user input.

    :return: (Result[Unit]) - Result indicating success or failure of the email sending operation.
    :rtype: Result[Unit]

    This function manages the email sending workflow by invoking a helper utility which manages sending emails
    to addresses provided through user input. It handles establishing the SMTP connection and delegates the
    actual email sending logic to the helper function.
    """
    # Invoke the helper utility to send emails to user-provided email addresses
    return run_email(
        lambda service: message_select_emails(service, build_custom_select_msg)
    )


def update_message_select(history: History) -> Result[Unit]:
    def _builder_intermediary() -> Result[TextBody]:
        return build_update_msg(history)

    return run_email(
        lambda server: message_select_emails(server, _builder_intermediary)
    )
