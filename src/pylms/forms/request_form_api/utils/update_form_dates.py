from pylms.models import (
    ChoiceQuestion,
    Content,
    CreateItem,
    Item,
    Location,
    OptionDict,
    Question,
    QuestionItem,
)
from pylms.record import RecordStatus


def new_content_from_date(selected_date: str, index: int) -> Content:
    return Content(
        createItem=CreateItem(
            item=Item(
                questionItem=QuestionItem(
                    question=Question(
                        choiceQuestion=ChoiceQuestion(
                            type="RADIO",
                            options=[
                                OptionDict(value=RecordStatus.PRESENT),
                                OptionDict(value=RecordStatus.ABSENT),
                                OptionDict(value=RecordStatus.EXCUSED),
                            ],
                            shuffle=False,
                        ),
                        required=True,
                    )
                ),
                title=f"Class {selected_date}",
                description=f"Please specify if you were present, absent from this class or if you were excused for the class on {selected_date}",
            ),
            location=Location(
                index=index,
            ),
        )
    )
