from typing import Literal, Optional

from pydantic import BaseModel


class DateQuestion(BaseModel):
    includeTime: bool = False
    includeYear: bool = True


class OptionDict(BaseModel):
    value: str


class ChoiceQuestion(BaseModel):
    type: Literal["DROP_DOWN", "RADIO", "TEXT"]
    options: list[OptionDict]
    shuffle: Optional[bool] = False


class TextQuestion(BaseModel):
    paragraph: Optional[bool] = False


class Question(BaseModel):
    required: bool
    choiceQuestion: Optional[ChoiceQuestion] = None
    textQuestion: Optional[TextQuestion] = None
    dateQuestion: Optional[DateQuestion] = None


class QuestionItem(BaseModel):
    question: Question


class Item(BaseModel):
    title: str
    description: Optional[str] = None
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
