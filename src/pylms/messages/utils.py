from typing import Callable, NamedTuple

from ..errors import Result


class TextBody(NamedTuple):
    title: str
    body: str


type MessageBuilder = Callable[[], Result[TextBody]]
