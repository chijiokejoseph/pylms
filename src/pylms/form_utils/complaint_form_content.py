from collections.abc import Generator
from datetime import datetime

from pylms.data import DataStore

from ..constants import (
    COHORT,
    CONFIRM_REG,
    CONFIRM_REG_STMT,
    COURSE,
    COURSES,
    COURSES_COMPLETE,
    COURSES_COMPLETE_STMT,
    DATE,
    DATE_FMT,
    EMAIL,
    EXPLANATION,
    EXPLANATION_STMT,
    ISSUE,
    ISSUES,
    MONTH_STR_FMT,
    NAME,
    PHONE,
    PROGRAM,
    PROGRAMS,
    REASON,
    WEEK_DAY_FMT,
)
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
    TextQuestion,
    counter_setup,
)


def new_complaint_form(ds: DataStore) -> ContentBody:
    cohort = ds.as_ref()[COHORT].astype(int).iloc[0]
    orientation = ds.as_ref()[DATE].astype(str).iloc[0]
    orientation = datetime.strptime(orientation, DATE_FMT)
    day, year = orientation.day, orientation.year

    def get_last(day: int) -> str:
        return str(day)[-1]

    last = get_last(day)
    match last:
        case "1":
            ext = "st"
        case "2":
            ext = "nd"
        case "3":
            ext = "rd"
        case _:
            ext = "th"

    month = orientation.strftime(MONTH_STR_FMT)
    weekday = orientation.strftime(WEEK_DAY_FMT)
    confirm_reg_stmt = (
        CONFIRM_REG_STMT
        + f" on {weekday}, the {day}{ext} of {month}, {year} for Cohort {cohort}"
    )

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
                        title=PHONE,
                        questionItem=QuestionItem(
                            question=Question(
                                textQuestion=TextQuestion(paragraph=False),
                                required=True,
                            )
                        ),
                        description="Enter your phone number. Please enter one by which you can be currently reached",
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=PROGRAM,
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="RADIO",
                                    shuffle=False,
                                    options=[
                                        OptionDict(value=program)
                                        for program in PROGRAMS
                                    ],
                                ),
                                required=True,
                            )
                        ),
                        description="Select your current program with NCAIR. If you are SIWES, pick the number of months you are expected to spend with NCAIR.",
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=COURSE,
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="CHECKBOX",
                                    shuffle=False,
                                    options=[
                                        OptionDict(value=course) for course in COURSES
                                    ]
                                    + [OptionDict(value="None")],
                                ),
                                required=True,
                            )
                        ),
                        description="Select the course(s) you registered for on the orientation day. If you did not register at all, select None.",
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=ISSUE,
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="RADIO",
                                    shuffle=False,
                                    options=[
                                        OptionDict(value=issue) for issue in ISSUES
                                    ],
                                ),
                                required=True,
                            )
                        ),
                        description="Which of these best describes your issue",
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=REASON,
                        questionItem=QuestionItem(
                            question=Question(
                                textQuestion=TextQuestion(paragraph=False),
                                required=True,
                            )
                        ),
                        description="State your reason if applicable",
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=EXPLANATION,
                        questionItem=QuestionItem(
                            question=Question(
                                textQuestion=TextQuestion(paragraph=False),
                                required=True,
                            )
                        ),
                        description=EXPLANATION_STMT,
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=CONFIRM_REG,
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="RADIO",
                                    shuffle=False,
                                    options=[
                                        OptionDict(value=option)
                                        for option in ["Yes", "No"]
                                    ],
                                ),
                                required=True,
                            )
                        ),
                        description=confirm_reg_stmt,
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=COURSES_COMPLETE,
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="CHECKBOX",
                                    shuffle=False,
                                    options=[
                                        OptionDict(value=course) for course in COURSES
                                    ]
                                    + [OptionDict(value="None (I am just starting)")],
                                ),
                                required=True,
                            )
                        ),
                        description=COURSES_COMPLETE_STMT,
                    ),
                    location=Location(index=next(counter)),
                )
            ),
        ]
    )
