from email.message import EmailMessage
from smtplib import SMTP

from pylms.config import Config

from ..cli import provide_emails
from ..email import MailError, run_email
from ..errors import Result, Unit
from ..history import History
from ..info import print_info, printpass
from .message import Message, MessageBody, MessageBodyBuilder
from .select_msg_builders import (
    compose_custom_msg_body,
    compose_update_msg_body,
)


def compose_message(
    config: Config, builder: MessageBodyBuilder
) -> Result[list[Message]]:
    """Build message records for selected email recipients.

    Args:
        config (Config): Configuration object containing admin email address.
        builder (MessageBuilder): Function to build message content.

    Returns:
        Result[list[MessageRecord]]: Success with message records or error.
    """

    # Retrieve the list of email addresses to send the message to
    emails = provide_emails()
    if emails.is_err():
        return emails.propagate()
    emails = emails.unwrap()

    # Initialize an empty list to hold the MessageRecord objects
    messages: list[Message] = []

    # Retrieve the sender's email address from environment variables
    sender: str = config.admin

    # Construct the HTML body of the email with styling and content
    msg_body = builder()
    if msg_body.is_err():
        return msg_body.propagate()
    msg_body = msg_body.unwrap()
    title, body = msg_body

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
        messages.append(Message(name=None, email=email, message=message))

    # Return the list of MessageRecord objects
    return Result.ok(messages)


def message_select_emails(
    server: SMTP, config: Config, builder: MessageBodyBuilder
) -> Result[Unit]:
    """Send emails to selected recipients using SMTP server.

    Args:
        server (SMTP): SMTP server instance for sending emails.
        config (Config): Configuration object containing admin email address.
        builder (MessageBuilder): Function to build message content.

    Returns:
        Result[Unit]: Success or error from email sending operation.
    """
    print_info("Initializing Sending Emails to provided emails...\n")

    errors: list[MailError] = []
    # retrieve the sender email from the environment
    sender: str = config.admin

    # get the messages to be sent by calling the passed in builder
    result = compose_message(config, builder)
    if result.is_err():
        # handle errors that occur during the building process
        return result.propagate()

    # get the list of messages to be sent
    messages: list[Message] = result.unwrap()

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


def custom_message_select(config: Config) -> Result[Unit]:
    """Send custom message to selected email addresses.

    Manages SMTP connection and delegates email sending to helper function.
    Message content is generated from user input.

    Args:
        config (Config): Configuration object containing admin email address.

    Returns:
        Result[Unit]: Success or error from email sending operation.
    """
    # Invoke the helper utility to send emails to user-provided email addresses
    return run_email(
        config,
        lambda service: message_select_emails(service, config, compose_custom_msg_body),
    )


def update_message_select(config: Config, history: History) -> Result[Unit]:
    """Send update message to selected email addresses.

    Args:
        config (Config): Configuration object containing email settings.
        history (History): History object for building update message.

    Returns:
        Result[Unit]: Success or error from email sending operation.
    """

    def _builder_intermediary() -> Result[MessageBody]:
        return compose_update_msg_body(history)

    return run_email(
        config,
        lambda server: message_select_emails(server, config, _builder_intermediary),
    )
