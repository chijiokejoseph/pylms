from email.message import EmailMessage
from typing import NamedTuple


class MessageRecord(NamedTuple):
    """Email message record containing recipient information and content.
    
    Attributes:
        name (str | None): Recipient name, or None if not provided.
        email (str): Recipient email address.
        message (EmailMessage): Email message content to be sent.
    """
    name: str | None
    email: str
    message: EmailMessage
