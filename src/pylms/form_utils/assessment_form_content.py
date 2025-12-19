from collections.abc import Generator

from ..constants import EMAIL, NAME
from ..models import (
    ChoiceQuestion,
    Content,
    ContentBody,
    CreateItem,
    Item,
    Location,
    OptionDict,
    Question,
    QuestionItem,
    counter_setup,
)


def new_assessment_content(names: list[str], emails: list[str]) -> ContentBody:
    counter: Generator[int, None, None] = counter_setup()
    return ContentBody(
        requests=[
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=NAME,
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="DROP_DOWN",
                                    shuffle=False,
                                    options=[OptionDict(value=name) for name in names],
                                ),
                                required=True,
                            )
                        ),
                        description="Select your name from the dropdown",
                    ),
                    location=Location(index=next(counter)),
                ),
            ),
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=EMAIL,
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="DROP_DOWN",
                                    shuffle=False,
                                    options=[
                                        OptionDict(value=email) for email in emails
                                    ],
                                ),
                                required=True,
                            )
                        ),
                        description="Select your name from the dropdown",
                    ),
                    location=Location(index=next(counter)),
                )
            ),
        ]
    )
