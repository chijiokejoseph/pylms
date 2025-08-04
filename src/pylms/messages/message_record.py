from email.message import EmailMessage
from typing import NamedTuple


class MessageRecord(NamedTuple):
    """
    Represents an email message record containing recipient information, 
    the email content and the recipient's name if provided.

    :ivar name: (str | None) - The name of the recipient, or None if not provided.
    :ivar email: (str) - The email address of the recipient.
    :ivar message: (EmailMessage) - The email message content to be sent.
    """
    name: str | None
    email: str
    message: EmailMessage
