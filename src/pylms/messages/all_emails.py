from email.message import EmailMessage
from smtplib import SMTP

from ..config import Config
from ..constants import COMMA_DELIM, EMAIL, GENDER, NAME, SPACE_DELIM
from ..data import DataStore
from ..email import MailError, run_email
from ..errors import Result, Unit
from ..history import History
from .all_msg_builders import (
    build_assessment_all_msg,
    build_custom_all_msg,
)
from .message_record import MessageRecord
from .utils import MessageBuilder, TextBody


def _construct_html_message(
    *, title: str, designation: str, name: str, body: str
) -> str:
    """Construct HTML email message with formatting.

    Args:
        title (str): Email title/subject.
        designation (str): Title prefix (Mr./Ms.).
        name (str): Recipient name.
        body (str): Message body content.

    Returns:
        str: Formatted HTML email content.
    """
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
    config: Config, ds: DataStore, builder: MessageBuilder
) -> Result[list[MessageRecord]]:
    """Build personalized email messages for each student in DataStore.

    Args:
        config (Config): Configuration object containing admin email address.
        ds (DataStore): DataStore containing student data.
        builder (MessageBuilder): Builder function to create message content.

    Returns:
        Result[list[MessageRecord]]: Success with list of message records or error.
    """
    # Get number of students in DataStore
    pretty = ds.pretty()
    nrows: int = pretty.height
    messages: list[MessageRecord] = []

    # Get sender email from environment
    sender: str = config.admin

    result: Result[TextBody] = builder()
    if result.is_err():
        return result.propagate()

    title, body = result.unwrap()

    # Create personalized message for each student
    for i in range(nrows):
        # Determine designation based on gender
        gender: str = pretty[i, GENDER]
        designation: str = (
            "Mr. "
            if gender.startswith("M")
            else "Ms. "
            if gender.startswith("F")
            else ""
        )

        # Get student name and email
        name: str = pretty[i, NAME].replace(COMMA_DELIM, SPACE_DELIM)
        email: str = pretty[i, EMAIL]

        # Create email message
        message: EmailMessage = EmailMessage()
        message["Subject"] = title
        message["From"] = sender

        # Construct HTML email content
        html_body = _construct_html_message(
            title=title, designation=designation, name=name, body=body
        )
        message.set_content(html_body, subtype="html")
        messages.append(MessageRecord(name=name, email=email, message=message))

    return Result.ok(messages)


def _message_all_emails(
    server: SMTP, config: Config, ds: DataStore, builder: MessageBuilder
) -> Result[Unit]:
    """Send personalized emails to all students using SMTP server.

    Args:
        server (SMTP): SMTP server instance for sending emails.
        config (Config): Configuration object containing admin email address.
        ds (DataStore): DataStore containing student data.
        builder (MessageBuilder): Function to build message content.

    Returns:
        Result[Unit]: Success or error message.
    """
    # Initialize error collection
    errors: list[MailError] = []
    sender: str = config.admin

    # Build messages for all students
    result: Result[list[MessageRecord]] = _build_all_message(config, ds, builder)
    if result.is_err():
        return result.propagate()

    messages: list[MessageRecord] = result.unwrap()

    # Send each message
    for i, message in enumerate(messages):
        name: str | None = message.name
        content: EmailMessage = message.message
        email: str = message.email
        try:
            # Send email via SMTP server
            err: MailError = server.send_message(
                content, from_addr=sender, to_addrs=email
            )
            # Check for sending errors
            if err != {}:
                errors.append({f"{i + 1}": (1, bytes(str(err), "utf-8"))})
                continue
            print(
                f"\nMail sent successfully to {f'{name} with ' if name is not None else ''}{email}\n"
            )
        except Exception as e:
            # Record any exceptions during sending
            errors.append({f"{i + 1}": (1, bytes(str(e), "utf-8"))})
            continue

    # Handle any errors that occurred
    if len(errors) > 0:
        for err in errors:
            for index in err:
                # Extract recipient info for error reporting
                i = int(index)
                err_name: str | None = messages[i - 1].name
                err_email: str = messages[i - 1].email
                # Print detailed error message
                if err_name is None:
                    err_print: str = f"{i}. Failed to send email to {err_email}"
                else:
                    err_print = f"{i}. Failed to send email to {err_name} with email: {err_email}"
                print(err_print)
            print()
        return result.propagate()

    return Result.unit()


def custom_message_all(config: Config, ds: DataStore) -> Result[Unit]:
    """Send custom message to all email addresses in DataStore.

    Initiates process of sending personalized messages to all recipients in the DataStore.
    Uses managed SMTP session to ensure proper connection handling.

    Args:
        config (Config): Configuration object containing admin email address.
        ds (DataStore): DataStore containing recipient information with gender, name, and email columns.

    Returns:
        Result[Unit]: Success or error from email sending operation.
    """
    return run_email(
        config,
        lambda service: _message_all_emails(
            service,
            config,
            ds,
            build_custom_all_msg,
        ),
    )


def assessment_message_all(
    config: Config, ds: DataStore, history: History
) -> Result[Unit]:
    """Send assessment message to all students.

    Args:
        config (Config): Configuration object containing admin email address.
        ds (DataStore): DataStore containing student data.
        history (History): History object for building assessment message.

    Returns:
        Result[Unit]: Success or error from email sending operation.
    """

    def _builder_intermediary() -> Result[TextBody]:
        return build_assessment_all_msg(history)

    return run_email(
        config,
        lambda service: _message_all_emails(service, config, ds, _builder_intermediary),
    )
