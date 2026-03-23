from email.message import EmailMessage
from typing import Callable, NamedTuple

from ..errors import Result


class Message(NamedTuple):
    """Email message details containing recipient information, optional sender and content.

    Attributes:
        name (str | None): Recipient name, or None if not provided.
        email (str): Recipient email address.
        message (EmailMessage): Email message content to be sent.
    """

    name: str | None
    email: str
    message: EmailMessage


class MessageBody(NamedTuple):
    """Text body container for email messages.

    Attributes:
        title (str): Email title/subject.
        body (str): Email body content.
    """

    title: str
    body: str


type MessageBodyBuilder = Callable[[], Result[MessageBody]]
"""Type alias for message builder functions.

Callable that returns a Result containing TextBody with title and body.
"""
