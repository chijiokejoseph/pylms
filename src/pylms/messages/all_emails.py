from pylms.utils import DataStore, must_get_env
from pylms.errors import Result, Unit
from smtplib import SMTP
from email.message import EmailMessage
from pylms.email import run_email, MailError
from pylms.messages.all_msg_builders import build_all_message
from pylms.messages.message_record import MessageRecord
from typing import Callable


def _message_all_emails(
    server: SMTP, builder: Callable[[], Result[list[MessageRecord]]]
) -> Result[Unit]:
    """
    Send personalized emails to all students using the provided SMTP server.

    :param server: (SMTP) - An SMTP server instance used to send emails.
    :type server: SMTP

    :param builder: (Callable[[], Result[list[MessageRecord]]]) - A callable that returns a Result containing a list of MessageRecord objects.
    :type builder: Callable[[], Result[list[MessageRecord]]]

    :return: (Result[Unit]) - returns a Result object indicating success or failure.
    :rtype: Result[Unit]
    """

    # Initialize a list to collect any mail errors
    errors: list[MailError] = []

    # Retrieve sender email from environment variables
    sender: str = must_get_env("EMAIL")

    # Call the builder function to get the list of messages to send
    result = builder()
    if result.is_err():
        # Return error result if builder failed
        return Result[Unit].err(result.unwrap_err())

    # Unwrap the result to get the list of MessageRecord objects
    messages: list[MessageRecord] = result.unwrap()

    # Iterate over each message and send it
    for i, message in enumerate(messages):
        content: EmailMessage = message.message
        email: str = message.email
        try:
            # Testing logic: override email for testing purposes
            email = "josephchijokeobodo@gmail.com"  # testing logic
            # Attempt to send the email via the SMTP server
            err: MailError = server.send_message(
                content, from_addr=sender, to_addrs=email
            )
            break  # testing logic
            # Check if there were any errors sending to this email
            if err != {}:
                # Append any errors to the errors list
                errors.append({f"{i + 1}": (1, bytes(str(err), "utf-8"))})
                continue
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
        return Result[Unit].err(ValueError("Failed to send emails"))

    # Return a success result if all emails were sent
    return Result[Unit].unit()


def custom_message_all_emails(ds: DataStore) -> Result[Unit]:
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

    # Define a builder function to create the list of messages to send
    def _all_msg_build() -> Result[list[MessageRecord]]:
        """
        custom builder function that captures the DataStore object to be used in the provided builder `build_all_message`

        :return: (Result[list[MessageRecord]]) - A result containing MessageRecord objects if successful else an error result
        :rtype: Result[list[MessageRecord]]
        """
        return build_all_message(ds)

    # Use run_email to establish SMTP connection and execute the email sending routine
    return run_email(lambda service: _message_all_emails(service, _all_msg_build))
