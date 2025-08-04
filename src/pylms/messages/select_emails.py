from pylms.utils import must_get_env
from pylms.errors import Result, Unit, ResultMap
from pylms.email import run_email, MailError
from email.message import EmailMessage
from smtplib import SMTP
from typing import Callable
from pylms.messages.message_record import MessageRecord
from pylms.messages.select_msg_builders import (
    build_select_message,
    build_update_form_msg,
)
from pylms.history import History


def _message_select_emails(
    server: SMTP, builder: Callable[[], Result[list[MessageRecord]]]
) -> Result[Unit]:
    """
    Send emails to a list of recipients selected through various input formats.

    :param server: (SMTP) - The SMTP server instance used to send emails.
    :type server: SMTP

    :param builder: (Callable[[], Result[list[MessageRecord]]]) -
                    A function that returns a list of MessageRecord objects.
    :type builder: Callable[[], Result[list[MessageRecord]]]

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
    result = builder()
    if result.is_err():
        # handle errors that occur during the building process
        return Result[Unit].err(result.unwrap_err())

    # get the list of messages to be sent
    messages: list[MessageRecord] = result.unwrap()

    # iterate over each message and send it
    for message in messages:
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
        except Exception as e:
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

    # If there were any errors, print them and return an error result
    if len(errors) > 0:
        for error in errors:
            for email in error:
                print(f"Failed to send to {email}")

        return Result[Unit].err(ValueError("Failed to send some emails"))
    # Return success result if all emails were sent without errors
    return Result[Unit].unit()


def custom_message_select_emails() -> Result[Unit]:
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
        lambda service: _message_select_emails(service, build_select_message)
    )


def _message_update_form(history: History, server: SMTP) -> Result[Unit]:
    """
    Send update form emails based on the provided history and SMTP server.

    :param history: (History) - History object containing data for building update form messages.
    :type history: History

    :param server: (SMTP) - The SMTP server instance used to send emails.
    :type server: SMTP

    :return: (Result[Unit]) - Result indicating success or failure of the email sending operation.
    :rtype: Result[Unit]

    This function builds update form messages from the given history, sends each email through the SMTP server,
    collects any errors encountered during sending, and reports them with detailed information including
    recipient name and email address.
    """
    result: Result[list[MessageRecord]] = build_update_form_msg(history)
    if result.is_err():
        # Return a successful result with no operation if building messages failed
        return ResultMap(result).map(lambda _: Unit())

    # Unwrap the result to get the list of MessageRecord objects
    messages: list[MessageRecord] = result.unwrap()

    errors: list[MailError] = []

    # get the sender from the environment
    sender: str = must_get_env("EMAIL")

    # iterate over each message and send it through the SMTP server
    for i, message in enumerate(messages):
        name, email, content = message
        try:
            # Attempt to send the email via the SMTP server
            err: MailError = server.send_message(
                content, from_addr=sender, to_addrs=email
            )
            # Collect any errors returned by the SMTP server
            if err != {}:
                errors.append(err)
        except Exception as e:
            # Catch exceptions during sending and record the error with index
            errors.append({email: (i + 1, bytes(str(e), "utf-8"))})
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
        return Result[Unit].err(ValueError("Failed to send emails"))

    # Return success result if all emails were sent without errors
    return Result[Unit].unit()


def message_update_form(history: History) -> Result[Unit]:
    return run_email(lambda service: _message_update_form(history, service))
