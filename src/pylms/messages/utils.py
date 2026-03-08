from typing import Callable, NamedTuple

from ..errors import Result


class TextBody(NamedTuple):
    """Text body container for email messages.

    Attributes:
        title (str): Email title/subject.
        body (str): Email body content.
    """

    title: str
    body: str


type MessageBuilder = Callable[[], Result[TextBody]]
"""Type alias for message builder functions.

Callable that returns a Result containing TextBody with title and body.
"""
