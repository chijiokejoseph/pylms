from collections.abc import Generator
from typing import Literal, Optional  # pyright: ignore[reportDeprecated]

from pydantic import BaseModel


def counter_setup(start: int = 0) -> Generator[int, None, None]:
    while True:
        yield start
        start += 1


class DateQuestion(BaseModel):
    includeTime: bool = False
    includeYear: bool = True


class OptionDict(BaseModel):
    value: str


class ChoiceQuestion(BaseModel):
    type: Literal["DROP_DOWN", "RADIO", "TEXT"]
    options: list[OptionDict]
    shuffle: Optional[bool] = False  # pyright: ignore[reportDeprecated]


class TextQuestion(BaseModel):
    paragraph: Optional[bool] = False  # pyright: ignore[reportDeprecated]


class Question(BaseModel):
    required: bool
    choiceQuestion: Optional[ChoiceQuestion] = None  # pyright: ignore[reportDeprecated]
    textQuestion: Optional[TextQuestion] = None  # pyright: ignore[reportDeprecated]
    dateQuestion: Optional[DateQuestion] = None  # pyright: ignore[reportDeprecated]


class QuestionItem(BaseModel):
    question: Question


class Item(BaseModel):
    title: str
    description: Optional[str] = None  # pyright: ignore[reportDeprecated]
    questionItem: QuestionItem


class Location(BaseModel):
    index: int


class CreateItem(BaseModel):
    item: Item
    location: Location


class Content(BaseModel):
    createItem: CreateItem


class ContentBody(BaseModel):
    requests: list[Content]
