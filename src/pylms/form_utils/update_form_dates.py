from ..models import (
    ChoiceQuestion,
    Content,
    CreateItem,
    Item,
    Location,
    OptionDict,
    Question,
    QuestionItem,
)
from ..record import RecordStatus


def new_content_from_date(selected_date: str, index: int) -> Content:
    """Create form content for attendance selection on a specific date.
    
    Args:
        selected_date (str): Date for the attendance question.
        index (int): Position index for the form field.
        
    Returns:
        Content: Form content with attendance options for the specified date.
    """
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
                title=f"{selected_date}",
                description=f"Please specify if you were present, absent from this class or if you were excused for the class on {selected_date}",
            ),
            location=Location(index=index),
        )
    )
