from typing import Optional  # pyright: ignore[reportDeprecated]

from pydantic import BaseModel


class Answer(BaseModel):
    value: str


class TextAnswer(BaseModel):
    answers: list[Answer]


class AnswerModel(BaseModel):
    questionId: str
    textAnswers: TextAnswer


class Response(BaseModel):
    responseId: str
    createTime: str
    lastSubmittedTime: str
    answers: dict[str, AnswerModel]


class ResponseModel(BaseModel):
    responses: Optional[list[Response]] = []  # pyright: ignore[reportDeprecated]
