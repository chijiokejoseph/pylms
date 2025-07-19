from datetime import datetime, timedelta
from pathlib import Path
from typing import Self
from pylms.errors import LMSError
from pylms.constants import HISTORY_PATH, DATE_FMT
from pylms.models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
import json


class HistoryError(LMSError):
    def __init__(self, message: str) -> None:
        return super().__init__(message)


class History:
    """A class to manage the history of classes, dates, and other related information.
    This class provides methods to load history data from a file, update dates based on class dates,
    and manage held and marked classes. It also allows extending the number of weeks in the history
    and adding held or marked classes based on class numbers.

    Attributes:
        class_dates (list[int]): A list of integers representing the weekdays on which classes are held.
            This should contain exactly 3 integers corresponding to the weekdays (0-6, where 0 is Monday).

        dates (list[datetime]): A list of datetime objects representing the dates of the classes.

        orientation_date (datetime | None): The date when the course starts.

        weeks (int): The number of weeks the course lasts.

        held_classes (list[datetime]): A list of datetime objects representing the classes for which attendance has been
            generated i.e., they have being held.

        marked_classes (list[datetime]): A list of datetime objects representing the for which attendance has been
            generated and have also being correspondingly recorded.

        cds_forms (list[CDSFormInfo]): A list of CDSFormInfo objects that store the details of all forms used to
            update cds day records

        update_forms (list[UpdateFormInfo]): A list of UpdateFormInfo objects that stored the details fo all forms used for
            onboarding students into the students record.

        attendance (tuple[bool, Path]): A tuple containing a boolean indicating whether attendance is recorded
            and the path to the attendance file.

        assessment (tuple[bool, Path]): A tuple containing a boolean indicating whether assessment is recorded
            and the path to the assessment file.

        project (tuple[bool, Path]): A tuple containing a boolean indicating whether the project is recorded
            and the path to the project file.

        result (tuple[bool, Path]): A tuple containing a boolean indicating whether the result is recorded
            and the path to the result file.

        _updated (bool): A boolean indicating whether the dates have been updated.
    """

    def __init__(self) -> None:
        self.class_dates: list[int] = []
        self.dates: list[datetime] = []
        self.orientation_date: datetime | None = None
        self.weeks: int = 5
        self.held_classes: list[datetime] = []
        self.marked_classes: list[datetime] = []
        self.class_forms: list[ClassFormInfo] = []
        self.recorded_class_forms: list[ClassFormInfo] = []
        self.cds_forms: list[CDSFormInfo] = []
        self.recorded_cds_forms: list[CDSFormInfo] = []
        self.update_forms: list[UpdateFormInfo] = []
        self.recorded_update_forms: list[UpdateFormInfo] = []
        self.attendance: tuple[bool, Path] = (False, Path())
        self.assessment: tuple[bool, Path] = (False, Path())
        self.project: tuple[bool, Path] = (False, Path())
        self.result: tuple[bool, Path] = (False, Path())
        self._updated: bool = False

    def _update_dates(self) -> None:
        """Updates the dates based on the class dates and orientation date.
        This method calculates the dates for the classes based on the class dates and the orientation date.
        It generates a list of dates for the entire duration of the course, ensuring that only the
        weekdays specified in `class_dates` are included.

        :param self: (History) - The instance of the History class.
        :type self: History

        :raises HistoryError: If class dates are not set or if the orientation date is not set.
        :raises HistoryError: If class dates do not contain exactly 3 integers.
        :raises HistoryError: If the orientation date is not set before updating dates.
        """
        if len(self.class_dates) != 3:
            raise HistoryError(
                "Class dates must contain exactly 3 integers corresponding to the weekdays on which classes are held."
            )
        if self.orientation_date is None:
            raise HistoryError("Start date must be set before updating dates.")

        all_dates: list[datetime] = [
            self.orientation_date + timedelta(days=i) for i in range(0, 7 * self.weeks)
        ]
        last_date: datetime = all_dates[-1]
        diff = 6 - last_date.weekday()
        dates_left: list[datetime] = [
            last_date + timedelta(days=i) for i in range(1, diff + 1)
        ]
        all_dates.extend(dates_left)
        self.dates = [date for date in all_dates if date.weekday() in self.class_dates]

        self._updated = True

    def str_dates(self) -> list[str]:
        return [datetime.strftime(date, DATE_FMT) for date in self.dates]

    @staticmethod
    def to_datetime(date_str: str) -> datetime:
        """Converts a date string to a datetime object.

        :param date_str: (str) - The date string to convert.
        :type date_str: str

        :return: (datetime) - The converted datetime object.
        :rtype: datetime

        :raises HistoryError: If the date string is not in the expected format.
        """
        try:
            return datetime.strptime(date_str, DATE_FMT)
        except ValueError:
            raise HistoryError(
                f"Invalid date format: {date_str}. Expected format is {DATE_FMT}."
            )

    @classmethod
    def load(cls) -> Self:
        """Loads the history data from a JSON file and initializes the History object.
        :return: (History) - An instance of the History class with loaded data.
        :rtype: History

        :raises HistoryError: If the history data is not in the expected format or if required fields are missing.
        """
        history = cls()

        if not HISTORY_PATH.exists():
            return history

        # Read the history data from the JSON file
        with HISTORY_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)

        # Validate the data format
        if not isinstance(data, dict):
            raise HistoryError("Invalid history data format.")

        # Check and set attribute `class_dates``
        if "class_dates" in data:
            if (
                not isinstance(data["class_dates"], list)
                or len(data["class_dates"]) != 3
            ):
                raise HistoryError("Class dates must be a list of exactly 3 integers.")
            if not all(isinstance(num, int) for num in data["class_dates"]):
                raise HistoryError("All class dates must be integers.")
            history.class_dates = [num for num in data["class_dates"]]

        # Check and set attribute `dates`
        if "dates" in data:
            if not isinstance(data["dates"], list):
                raise HistoryError("Dates must be a list of date strings.")
            history.dates = [cls.to_datetime(date_str) for date_str in data["dates"]]

        # Check and set attribute `orientation_date`
        if "orientation_date" in data:
            history.orientation_date = cls.to_datetime(data["orientation_date"])

        # Check and set attribute `weeks`
        if "weeks" in data:
            if not isinstance(data["weeks"], int) or data["weeks"] < 1:
                raise HistoryError("Weeks must be a positive integer.")
            history.weeks = data["weeks"]

        # Check and set attribute `held_classes`
        if "held_classes" in data:
            if not isinstance(data["held_classes"], list):
                raise HistoryError("Held classes must be a list of date strings.")
            history.held_classes = [
                cls.to_datetime(date_str) for date_str in data["held_classes"]
            ]

        # Check and set attribute `marked_classes`
        if "marked_classes" in data:
            if not isinstance(data["marked_classes"], list):
                raise HistoryError("Marked classes must be a list of date strings.")
            history.marked_classes = [
                cls.to_datetime(date_str) for date_str in data["marked_classes"]
            ]

        # Check and set attribute `class_forms`
        if "class_forms" in data:
            if not isinstance(data["class_forms"], list) and not isinstance(
                data["class_forms"][0], dict
            ):
                raise HistoryError("Class forms must be a list of dictionaries")
            history.class_forms = [
                ClassFormInfo.model_validate(info) for info in data["class_forms"]
            ]

        # Check and set attribute `recorded_class_forms`
        if "recorded_class_forms" in data:
            if not isinstance(data["recorded_class_forms"], list) and not isinstance(
                data["recorded_class_forms"][0], dict
            ):
                raise HistoryError("Class forms must be a list of dictionaries")
            history.recorded_class_forms = [
                ClassFormInfo.model_validate(info)
                for info in data["recorded_class_forms"]
            ]

        # Check and set attribute `cds_forms`
        if "cds_forms" in data:
            if not isinstance(data["cds_forms"], list) and not isinstance(
                data["cds_forms"][0], dict
            ):
                raise HistoryError("CDS forms must be a list of dictionaries")
            history.cds_forms = [
                CDSFormInfo.model_validate(info) for info in data["cds_forms"]
            ]

        # Check and set attribute `recorded_cds_forms`
        if "recorded_cds_forms" in data:
            if not isinstance(data["recorded_cds_forms"], list) and not isinstance(
                data["recorded_cds_forms"][0], dict
            ):
                raise HistoryError("CDS forms must be a list of dictionaries")
            history.recorded_cds_forms = [
                CDSFormInfo.model_validate(info) for info in data["recorded_cds_forms"]
            ]

        # Check and set attribute `update_forms`
        if "update_forms" in data:
            if not isinstance(data["update_forms"], list) and not isinstance(
                data["update_forms"][0], dict
            ):
                raise HistoryError("Update forms must be a list of dictionaries")
            history.update_forms = [
                UpdateFormInfo.model_validate(info) for info in data["update_forms"]
            ]

        # Check and set attribute `recorded_update_forms`
        if "recorded_update_forms" in data:
            if not isinstance(data["recorded_update_forms"], list) and not isinstance(
                data["recorded_update_forms"][0], dict
            ):
                raise HistoryError("Update forms must be a list of dictionaries")
            history.recorded_update_forms = [
                UpdateFormInfo.model_validate(info)
                for info in data["recorded_update_forms"]
            ]

        # Check and set attributes `attendance`, `assessment`, `project`, and `result`
        if "attendance" in data:
            if not isinstance(data["attendance"], list) or len(data["attendance"]) != 2:
                raise HistoryError(
                    "Attendance must be a list with two elements: a boolean and a file path."
                )
            history.attendance = (data["attendance"][0], Path(data["attendance"][1]))

        if "assessment" in data:
            if not isinstance(data["assessment"], list) or len(data["assessment"]) != 2:
                raise HistoryError(
                    "Assessment must be a list with two elements: a boolean and a file path."
                )
            history.assessment = (data["assessment"][0], Path(data["assessment"][1]))

        if "project" in data:
            if not isinstance(data["project"], list) or len(data["project"]) != 2:
                raise HistoryError(
                    "Project must be a list with two elements: a boolean and a file path."
                )
            history.project = (data["project"][0], Path(data["project"][1]))

        if "result" in data:
            if not isinstance(data["result"], list) or len(data["result"]) != 2:
                raise HistoryError(
                    "Result must be a list with two elements: a boolean and a file path."
                )
            history.result = (data["result"][0], Path(data["result"][1]))

        # Update the dates based on the loaded data
        history._update_dates()

        return history

    def save(self) -> None:
        """Saves the current history data to a JSON file.

        :return: (None) - This method does not return anything.
        :rtype: None

        :raises HistoryError: If the history data is not in the expected format or if required fields are missing.
        """
        data = {
            "class_dates": list(self.class_dates),
            "dates": [date.strftime(DATE_FMT) for date in self.dates],
            "orientation_date": self.orientation_date.strftime(DATE_FMT)
            if self.orientation_date
            else None,
            "weeks": self.weeks,
            "held_classes": [date.strftime(DATE_FMT) for date in self.held_classes],
            "marked_classes": [date.strftime(DATE_FMT) for date in self.marked_classes],
            "class_forms": [data.model_dump(mode="json") for data in self.class_forms],
            "recorded_class_forms": [
                data.model_dump(mode="json") for data in self.recorded_class_forms
            ],
            "cds_forms": [data.model_dump(mode="json") for data in self.cds_forms],
            "recorded_cds_forms": [
                data.model_dump(mode="json") for data in self.recorded_cds_forms
            ],
            "update_forms": [
                data.model_dump(mode="json") for data in self.update_forms
            ],
            "recorded_update_forms": [
                data.model_dump(mode="json") for data in self.recorded_update_forms
            ],
            "attendance": [self.attendance[0], str(self.attendance[1])],
            "assessment": [self.assessment[0], str(self.assessment[1])],
            "project": [self.project[0], str(self.project[1])],
            "result": [self.result[0], str(self.result[1])],
        }

        with HISTORY_PATH.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def extend_weeks(self, additional_weeks: int) -> None:
        """Extends the number of weeks in the history.

        :param additional_weeks: (int) - The number of additional weeks to extend.
        :type additional_weeks: int

        :return: (None) - This method does not return anything.
        :rtype: None

        :raises HistoryError: If additional weeks is a negative integer.
        """
        if additional_weeks < 0:
            raise HistoryError("Additional weeks must be a non-negative integer.")
        self.weeks += additional_weeks
        self._update_dates()

    def add_held_class(
        self, *, class_num: int | None = None, class_date: str | None = None
    ) -> None:
        """Adds a held class based on the class number.

        :param class_num: (int) - The
            class number to add as a held class.
        :type class_num: int

        :return: (None) - This method does not return anything.
        :rtype: None

        :raises HistoryError: If the dates have not been updated or if the class number is out of range.
        """
        # Ensure that dates have been updated before adding held classes
        if not self._updated:
            raise HistoryError("Dates must be updated before adding held classes.")

        if class_num is None and class_date is None:
            raise HistoryError(
                "one of the arguments `class_num` and `class_date` must be specified"
            )

        # Check if the class number is within the valid range
        if class_num is not None and (class_num < 1 or class_num > len(self.dates)):
            raise HistoryError(f"Class number {class_num} is out of range.")

        if class_date is not None and class_date not in self.str_dates():
            raise HistoryError(
                f"Class Date: {class_date} is not part of the valid dates list for this program."
            )

        # Get the date corresponding to the class number and add it to held classes
        held_date: datetime | None = (
            list(self.dates)[class_num - 1]
            if class_num is not None
            else History.to_datetime(class_date)
            if class_date is not None
            else None
        )
        if held_date is None:
            raise HistoryError("")
        self.held_classes.append(held_date)

    def add_marked_class(self, class_num: int) -> None:
        """Adds a marked class based on the class number.

        :param class_num: (int) - The
            class number to add as a marked class.
        :type class_num: int

        :return: (None) - This method does not return anything.
        :rtype: None

        :raises HistoryError: If the dates have not been updated or if the class number is out of range.
        """
        # Ensure that dates have been updated before adding marked classes
        if not self._updated:
            raise HistoryError("Dates must be updated before adding marked classes.")

        # Check if the class number is within the valid range
        if class_num < 1 or class_num > len(self.dates):
            raise HistoryError(f"Class number {class_num} is out of range.")

        # Get the date corresponding to the class number and add it to marked classes
        class_date = list(self.dates)[class_num - 1]

        # Check if the class has been held before marking it
        if class_date not in self.held_classes:
            raise HistoryError(f"Class {class_num} has not been held yet.")
        self.marked_classes.append(class_date)

    def add_cds_form(self, form: CDSFormInfo) -> None:
        self.cds_forms.append(form)

    def add_recorded_cds_form(self, form: CDSFormInfo) -> None:
        self.recorded_cds_forms.append(form)

    def add_update_form(self, form: UpdateFormInfo) -> None:
        self.update_forms.append(form)

    def add_recorded_update_form(self, form: UpdateFormInfo) -> None:
        self.recorded_update_forms.append(form)

    def add_class_form(self, form: ClassFormInfo) -> None:
        self.class_forms.append(form)

    def add_recorded_class_form(self, form: ClassFormInfo) -> None:
        self.recorded_class_forms.append(form)

    def get_available_class_forms(self) -> list[ClassFormInfo]:
        return [
            form for form in self.class_forms if form not in self.recorded_class_forms
        ]

    def get_available_cds_forms(self) -> list[CDSFormInfo]:
        return [form for form in self.cds_forms if form not in self.recorded_cds_forms]

    def get_available_update_forms(self) -> list[UpdateFormInfo]:
        return [
            form for form in self.update_forms if form not in self.recorded_update_forms
        ]
        
    def match_info_by_date(self, class_date: str) -> ClassFormInfo:
        return [form for form in self.class_forms if form.date == class_date][0]
        
