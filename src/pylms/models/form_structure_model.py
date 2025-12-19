# pyright: reportDeprecated=false

from typing import Optional

from pydantic import BaseModel

from .setup_form_data import ChoiceQuestion, TextQuestion


class QuestionDetails(BaseModel):
    questionId: str
    required: bool
    textQuestion: Optional[TextQuestion] = None
    choiceQuestion: Optional[ChoiceQuestion] = None


class QuestionItem(BaseModel):
    question: QuestionDetails


class ItemsModel(BaseModel):
    itemId: str
    title: str
    description: Optional[str] = None
    questionItem: QuestionItem


class FormInfo(BaseModel):
    title: str
    documentTitle: str


class FormModel(BaseModel):
    formId: str
    info: FormInfo
    settings: dict[str, str]
    revisionId: str
    responderUri: str
    items: list[ItemsModel]
