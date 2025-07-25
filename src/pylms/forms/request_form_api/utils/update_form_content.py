from typing import Generator

from pylms.constants import (
    CDS,
    COMPLETION,
    WORK_DAYS,
    EMAIL,
    GENDER,
    INTERNSHIP,
    NAME,
    PHONE,
)
from pylms.forms.request_form_api.utils.update_form_dates import new_content_from_date
from pylms.models import (
    ChoiceQuestion,
    Content,
    ContentBody,
    CreateItem,
    DateQuestion,
    Item,
    Location,
    OptionDict,
    Question,
    QuestionItem,
    TextQuestion,
    counter_setup
)


def new_content_body(dates_list: list[str]) -> ContentBody:
    counter: Generator[int, None, None] = counter_setup()

    content_body: ContentBody = ContentBody(
        requests=[
            # Name
            Content(
                createItem=CreateItem(
                    item=Item(
                        questionItem=QuestionItem(
                            question=Question(
                                textQuestion=TextQuestion(paragraph=False),
                                required=True,
                            )
                        ),
                        description="Enter your name in the order: Last Name, First Name, Middle Name",
                        title=NAME,
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            # Gender
            Content(
                createItem=CreateItem(
                    item=Item(
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="RADIO",
                                    options=[
                                        OptionDict(value="Male"),
                                        OptionDict(value="Female"),
                                    ],
                                    shuffle=False,
                                ),
                                required=True,
                            )
                        ),
                        title=GENDER,
                    ),
                    location=Location(
                        index=next(counter),
                    ),
                )
            ),
            # Email
            Content(
                createItem=CreateItem(
                    item=Item(
                        questionItem=QuestionItem(
                            question=Question(
                                textQuestion=TextQuestion(paragraph=False),
                                required=True,
                            )
                        ),
                        description="Enter your email",
                        title=EMAIL,
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            # Phone
            Content(
                createItem=CreateItem(
                    item=Item(
                        questionItem=QuestionItem(
                            question=Question(
                                textQuestion=TextQuestion(paragraph=False),
                                required=True,
                            )
                        ),
                        description="Enter your phone number: Please ensure that your phone numbers match the following samples \ni. Single Phone number: 09076025342 \nii. Multiple Phone numbers: 09065543321, 08122345278, ... \nThank you.",
                        title=PHONE,
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            # Internship
            Content(
                createItem=CreateItem(
                    item=Item(
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="RADIO",
                                    options=[
                                        OptionDict(value="NYSC"),
                                        OptionDict(value="SIWES"),
                                    ],
                                    shuffle=False,
                                ),
                                required=True,
                            )
                        ),
                        title=INTERNSHIP,
                    ),
                    location=Location(
                        index=next(counter),
                    ),
                )
            ),
            # Completion
            Content(
                createItem=CreateItem(
                    item=Item(
                        questionItem=QuestionItem(
                            question=Question(
                                dateQuestion=DateQuestion(),
                                required=True,
                            )
                        ),
                        description="Enter the date you are expected to finish your internship (applies to both SIWES and NYSC)",
                        title=COMPLETION,
                    ),
                    location=Location(index=next(counter)),
                )
            ),
            # CDS
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=CDS,
                        description="Select your CDS Day",
                        questionItem=QuestionItem(
                            question=Question(
                                required=True,
                                choiceQuestion=ChoiceQuestion(
                                    type="RADIO",
                                    shuffle=False,
                                    options=[
                                        OptionDict(value=day)
                                        for day in WORK_DAYS + ["None"]
                                    ],
                                ),
                            )
                        ),
                    ),
                    location=Location(index=next(counter)),
                )
            ),
        ]
    )

    for date in dates_list:
        content_body.requests.append(new_content_from_date(date, next(counter)))
    return content_body
