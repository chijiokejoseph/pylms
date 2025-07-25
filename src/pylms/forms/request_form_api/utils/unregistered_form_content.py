from pylms.constants import NAME, EMAIL, COURSES
from pylms.models import (
    ContentBody,
    Content,
    CreateItem,
    Item,
    QuestionItem,
    Question,
    TextQuestion,
    ChoiceQuestion,
    OptionDict,
    Location,
    counter_setup,
)
from typing import Generator


def new_content_body() -> ContentBody:
    counter: Generator[int, None, None] = counter_setup()
    return ContentBody(
        requests=[
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=NAME,
                        questionItem=QuestionItem(
                            question=Question(
                                textQuestion=TextQuestion(paragraph=False),
                                required=True,
                            )
                        ),
                        description="Enter your name in the order: Last Name, First Name, Middle Name",
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=EMAIL,
                        questionItem=QuestionItem(
                            question=Question(
                                textQuestion=TextQuestion(paragraph=False),
                                required=True,
                            )
                        ),
                        description="Enter a valid email address (preferrably GMAIL)",
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            Content(
                createItem=CreateItem(
                    item=Item(
                        title="Course",
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="DROP_DOWN",
                                    shuffle=False,
                                    options=[
                                        OptionDict(value=course) for course in COURSES
                                    ]
                                    + [OptionDict(value="None")],
                                ),
                                required=True,
                            )
                        ),
                        description="Select the course you registered for on the orientation day. If you did not register at all, select None.",
                    ),
                    location=Location(index=next(counter)),
                )
            ),
        ]
    )
