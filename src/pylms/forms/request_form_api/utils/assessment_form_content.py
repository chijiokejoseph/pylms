from pylms.constants import NAME
from pylms.models import (
    ContentBody,
    Content,
    CreateItem,
    Item,
    QuestionItem,
    Question,
    ChoiceQuestion,
    OptionDict,
    Location,
    counter_setup,
)
from typing import Generator


def new_content_body(names: list[str]) -> ContentBody:
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
                )
            ),
        ]
    )
