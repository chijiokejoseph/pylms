from ..constants import NAME
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


def new_assessment_content(fmt_names: list[str]) -> ContentBody:
    """Create content body for assessment form with name and email dropdowns.

    Args:
        fmt_names (list[str]): List of student names for dropdown.

    Returns:
        ContentBody: Form content with name and email selection fields.
    """
    counter = counter_setup()
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
                                    options=[
                                        OptionDict(value=name) for name in fmt_names
                                    ],
                                ),
                                required=True,
                            )
                        ),
                        description="Select your name from the dropdown",
                    ),
                    location=Location(index=next(counter)),
                ),
            ),
        ]
    )
