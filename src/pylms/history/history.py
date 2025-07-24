from datetime import datetime, timedelta
from pathlib import Path
from typing import Self, cast
from pylms.errors import LMSError
from pylms.constants import DATE_FMT, HISTORY_PATH, DATE, WEEK_DAYS, COHORT
from pylms.models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from pylms.utils import paths, DataStore
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
        cohort (int | None): The cohort number.

        class_days (list[int]): A list of integers representing the weekdays on which classes are held.
            This should contain exactly 3 integers corresponding to the weekdays (0-6, where 0 is Monday).

        dates (list[datetime]): A list of datetime objects representing the dates of the classes.

        orientation_date (datetime | None): The date when the course starts.

        weeks (int): The number of weeks the course lasts.

        held_classes (list[datetime]): A list of datetime objects representing the classes for which attendance has been
            generated i.e., they have being held.

        marked_classes (list[datetime]): A list of datetime objects representing the for which attendance has been
            generated and have also being correspondingly recorded.

        class_forms (list[ClassFormInfo]): A list of ClassFormInfo objects that store the details of all forms used to
            generate attendance records

        recorded_class_forms (list[ClassFormInfo]): A list of ClassFormInfo objects that stored the details fo all forms used for
            generating attendance records that have been recorded

        cds_forms (list[CDSFormInfo]): A list of CDSFormInfo objects that store the details of all forms used to
            update cds day records

        recorded_cds_forms (list[CDSFormInfo]): A list of CDSFormInfo objects that stored the details fo all forms used for
            onboarding students into the students record that have been recorded

        update_forms (list[UpdateFormInfo]): A list of UpdateFormInfo objects that stored the details fo all forms used for
            onboarding students into the students record

        recorded_update_forms (list[UpdateFormInfo]): A list of UpdateFormInfo objects that stored the details fo all forms
            used for onboarding students into the students record that have been recorded

        attendance (tuple[bool, Path]): A tuple containing a boolean indicating whether attendance is recorded
            and the path to the attendance file.

        assessment (tuple[bool, Path]): A tuple containing a boolean indicating whether assessment is recorded
            and the path to the assessment file.

        project (tuple[bool, Path]): A tuple containing a boolean indicating whether the project is recorded
            and the path to the project file.

        result (tuple[bool, Path]): A tuple containing a boolean indicating whether the result is recorded
            and the path to the result file.

        merit (tuple[bool, Path]): A tuple containing a boolean indicating whether the merit awardees has been recorded
            and the path to the merit awardees file.

        _updated (bool): A boolean indicating whether the dates have been updated.
    """

    def __init__(self) -> None:
        self.cohort: int | None = None
        self.class_days: list[int] = []
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
        self.merit: tuple[bool, Path] = (False, Path())
        self._updated: bool = False

    def _update_dates(self) -> None:
        """
        Updates the dates based on the class dates and orientation date.

        This method calculates the dates for the classes based on the class dates and the orientation date.
        It generates a list of dates for the entire duration of the course, ensuring that only the
        weekdays specified in ``class_dates`` are included.

        :param self: (History) - The instance of the History class.
        :type self: History

        :raises HistoryError: If class dates are not set or if the orientation date is not set.
        :raises HistoryError: If class dates do not contain exactly 3 integers.
        :raises HistoryError: If the orientation date is not set before updating dates.

        :return: None
        :rtype: None
        """
        # Validate that exactly three class weekdays are specified
        if len(self.class_days) != 3:
            raise HistoryError(
                "Class dayss must contain exactly 3 integers corresponding to the weekdays on which classes are held."
            )
        # Ensure the orientation date is set before proceeding
        if self.orientation_date is None:
            raise HistoryError("Orientation date must be set before updating dates.")

        # Generate all dates for the course duration, starting from the day after orientation
        all_dates: list[datetime] = [
            self.orientation_date + timedelta(days=i) for i in range(1, 7 * self.weeks)
        ]

        # Identify the last date in the generated range
        last_date: datetime = all_dates[-1]

        # Calculate how many days remain in the final week to reach the next Sunday
        diff = 6 - last_date.weekday()

        # Generate the remaining dates to complete the final week
        dates_left: list[datetime] = [
            last_date + timedelta(days=i) for i in range(1, diff + 1)
        ]

        # Extend the list of all dates to include the remaining days in the final week
        all_dates.extend(dates_left)

        # Filter all dates to include only those that match the specified class weekdays
        self.dates = [date for date in all_dates if date.weekday() in self.class_days]

        # Mark the dates as updated
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
        history_path: Path = paths.get_history_path()

        if not history_path.exists():
            return history

        # Read the history data from the JSON file
        with history_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        # Validate the data format
        if not isinstance(data, dict):
            raise HistoryError("Invalid history data format.")

        # Check and set attribute `cohort`
        if "cohort" in data:
            if not isinstance(data["cohort"], int):
                raise HistoryError("Cohort must be an integer.")
            history.cohort = data["cohort"]

        # Check and set attribute `class_days`
        if "class_days" in data:
            if not isinstance(data["class_days"], list) or len(data["class_days"]) != 3:
                raise HistoryError("Class dates must be a list of exactly 3 integers.")
            if not all(isinstance(num, int) for num in data["class_days"]):
                raise HistoryError("All class dates must be integers.")
            history.class_days = [num for num in data["class_days"]]

        # Check and set attribute `dates`
        if "dates" in data:
            if not isinstance(data["dates"], list):
                raise HistoryError("Dates must be a list of date strings.")
            history.dates = [cls.to_datetime(date_str) for date_str in data["dates"]]

        # Check and set attribute `orientation_date`
        if "orientation_date" in data and data["orientation_date"] is not None:
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

        if "merit" in data:
            if not isinstance(data["merit"], list) or len(data["merit"]) != 2:
                raise HistoryError(
                    "Merit must be a list with two elements: a boolean and a file path."
                )
            history.merit = (data["merit"][0], Path(data["merit"][1]))

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
            # Cohort number
            "cohort": self.cohort,
            # List of 3 integers representing weekdays on which classes are held
            "class_days": list(self.class_days),
            # List of 3 integers representing weekdays on which classes are marked
            "dates": [date.strftime(DATE_FMT) for date in self.dates],
            # orientation date in the format specified by DATE_FMT or None
            "orientation_date": self.orientation_date.strftime(DATE_FMT)
            if self.orientation_date
            else None,
            # Number of weeks the course lasts
            "weeks": self.weeks,
            # List of classes for which attendance has been generated
            "held_classes": [date.strftime(DATE_FMT) for date in self.held_classes],
            # List of classes for which attendance has been marked
            "marked_classes": [date.strftime(DATE_FMT) for date in self.marked_classes],
            # List of dictionaries representing ClassFormInfo objects
            "class_forms": [data.model_dump(mode="json") for data in self.class_forms],
            # List of dictionaries representing ClassFormInfo objects for
            # recorded classes
            "recorded_class_forms": [
                data.model_dump(mode="json") for data in self.recorded_class_forms
            ],
            # List of dictionaries representing CDSFormInfo objects
            "cds_forms": [data.model_dump(mode="json") for data in self.cds_forms],
            # List of dictionaries representing CDSFormInfo objects
            # for recorded CDS forms
            "recorded_cds_forms": [
                data.model_dump(mode="json") for data in self.recorded_cds_forms
            ],
            # List of dictionaries representing UpdateFormInfo objects
            "update_forms": [
                data.model_dump(mode="json") for data in self.update_forms
            ],
            # List of dictionaries representing UpdateFormInfo objects
            # for recorded update forms
            "recorded_update_forms": [
                data.model_dump(mode="json") for data in self.recorded_update_forms
            ],
            "attendance": [
                self.attendance[0],
                str(self.attendance[1]),
            ],  # List of boolean and file path
            "assessment": [
                self.assessment[0],
                str(self.assessment[1]),
            ],  # List of boolean and file path
            "project": [
                self.project[0],
                str(self.project[1]),
            ],  # List of boolean and file path
            "result": [
                self.result[0],
                str(self.result[1]),
            ],  # List of boolean and file path
            "merit": [
                self.merit[0],
                str(self.merit[1]),
            ],  # List of boolean and file path
        }

        # Save the history data to the JSON file
        with paths.get_history_path().open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        # Save the history data to the JSON file
        with HISTORY_PATH.open("w") as file:
            json.dump(data, file, indent=2)

        # Save the dates to the JSON file (`Json/dates.json`)
        # if the dates have changed

        dates_json_list: list[str] = []

        # Load the dates from the JSON file `Json/dates.json`
        dates_json_path: Path = paths.get_paths_json()["Date"]
        with dates_json_path.open("r") as file:
            dates_json_list.extend(json.load(file))

        # Update the dates in the JSON file if they have changed
        if dates_json_list != self.str_dates():
            with dates_json_path.open("w") as file:
                json.dump(self.str_dates(), file, indent=2)

    def set_cohort(self, ds: DataStore) -> None:
        self.orientation_date = datetime.strptime(
            ds.data[DATE].astype(str).iloc[0], DATE_FMT
        )
        self.cohort = ds.data[COHORT].astype(int).iloc[0]
        self._update_dates()

    def set_class_days(
        self,
        days: list[int] | list[str],
        *,
        start: int | None,
    ) -> None:
        """
        Sets the class days for the schedule.

        This method validates and sets the days of the week on which classes are held.
        The days parameter must contain exactly three unique elements, either as integers
        (weekday indices) or as strings (weekday names). If integers are provided, a start
        index must also be specified. If strings are provided, they must match entries in
        the WEEK_DAYS list.

        :param self: (History) - The instance of the History class.
        :type self: History
        :param days: (SupportsLenGetitem[int] | SupportsLenGetitem[str]) - A sequence of exactly 3 elements, each representing a weekday.
            If elements are integers, they represent weekday indices (e.g., 0 for Monday).
            If elements are strings, they must match entries in WEEK_DAYS (e.g., "Monday").
        :type days: SupportsLenGetitem[int] | SupportsLenGetitem[str]
        :param start: (int | None) - The starting weekday index. Required if `days` contains integers.
        :type start: int | None

        :return: (None) - returns nothing
        :rtype: None

        :raises HistoryError: If `days` does not contain exactly 3 elements.
        :raises HistoryError: If any elements in `days` are not unique.
        :raises HistoryError: If `days` contains integers and `start` is not provided.
        :raises HistoryError: If `days` contains strings not matching WEEK_DAYS.
        :raises HistoryError: If `days` is not a list of valid integers or strings.
        """
        # Ensure exactly three days are provided
        if len(days) != 3:
            raise HistoryError(
                "Class days must contain exactly 3 integers corresponding to the weekdays on which classes are held."
            )

        # Ensure all days are unique
        if days[0] == days[1] or days[0] == days[2] or days[1] == days[2]:
            raise HistoryError(
                "Class days must contain unique integers corresponding to the weekdays on which classes are held."
            )

        # Determine the type of input and process accordingly
        match True:
            # If integers are provided and a start index is given, calculate weekday indices
            case _ if all(isinstance(day, int) for day in days) and start is not None:
                # Subtract start from each integer to normalize to weekday indices
                self.class_days = [cast(int, i) - start for i in days]

            # If strings are provided and all are valid weekday names, convert to indices
            case _ if all(isinstance(day, str) for day in days) and all(
                cast(str, day).title() in WEEK_DAYS for day in days
            ):
                # Map weekday names to their indices
                self.class_days = [WEEK_DAYS.index(cast(str, day)) for day in days]

            # If integers are provided but no start index, raise an error
            case _ if all(isinstance(day, int) for day in days) and start is None:
                raise HistoryError("Start must be provided if first is an integer.")

            # If strings are provided but not all are valid weekday names, raise an error
            case _ if all(isinstance(day, str) for day in days) and not all(
                day in WEEK_DAYS for day in days
            ):
                raise HistoryError(
                    "Days must be a list of strings corresponding to the weekdays on which classes are held, and must match the following list {WEEK_DAYS}."
                )

            # For any other invalid input, raise an error
            case _:
                raise HistoryError(
                    "Days must be a list of integers or strings corresponding to the weekdays on which classes are held, and must match the following list {WEEK_DAYS}."
                )

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

    def replan_weeks(self, new_weeks: int) -> None:
        """Replans the number of weeks in the history.

        This method sets a new number of weeks for the course and updates the relevant dates
        based on the new duration.

        :param new_weeks: (int) - The new number of weeks for the course.
        :type new_weeks: int

        :return: (None) - This method does not return anything.
        :rtype: None

        :raises HistoryError: If the new number of weeks is less than or equal to 1.
        """

        if new_weeks <= 1:
            raise HistoryError("Number of weeks must be greater than 1.")

        self.weeks = new_weeks
        self._update_dates()

    def add_held_class(
        self, *, class_num: int | None = None, class_date: str | None = None
    ) -> None:
        """Adds a held class based on the class number. Either class_num or class_date must be specified, else an error will be raised.

        :param class_num: (int | None) - The
            class number to add as a held class. Defaults to None.
        :type class_num: int | None

        :param class_date: (str | None) - The
            class date to add as a held class. Defaults to None.
        :type class_date: str | None

        :return: (None) - This method does not return anything.
        :rtype: None

        :raises HistoryError: If class_num and class_date are both None or if the class_num is out of range.
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

    def add_marked_class(
        self, class_num: int | None = None, class_date: str | None = None
    ) -> None:
        """Adds a marked class based on the class number. Either class_num or class_date must be specified, else an error will be raised.

        :param class_num: (int | None) - The
            class number to add as a held class. Defaults to None.
        :type class_num: int | None

        :param class_date: (str | None) - The
            class date to add as a held class. Defaults to None.
        :type class_date: str | None

        :return: (None) - This method does not return anything.
        :rtype: None

        :raises HistoryError: If class_num and class_date are both None or if the class_num is out of range.
        """
        # Ensure that dates have been updated before adding marked classes
        if not self._updated:
            raise HistoryError("Dates must be updated before adding marked classes.")

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
        marked_date: datetime | None = (
            list(self.dates)[class_num - 1]
            if class_num is not None
            else History.to_datetime(class_date)
            if class_date is not None
            else None
        )

        # Check if the class has been held before marking it
        if marked_date is None:
            raise HistoryError("")
        self.marked_classes.append(marked_date)

    def add_cds_form(self, form: CDSFormInfo) -> None:
        """
        Adds a CDS Form to the list of CDS forms.

        :param form: (CDSFormInfo) - The CDS Form to add.
        :type form: CDSFormInfo
        :return: (None) - This method does not return anything.
        :rtype: None
        """
        self.cds_forms.append(form)

    def add_recorded_cds_form(self, form: CDSFormInfo) -> None:
        """
        Adds a recorded CDS Form to the list of recorded CDS forms.

        :param form: (CDSFormInfo) - The recorded CDS Form to add.
        :type form: CDSFormInfo
        :return: (None) - This method does not return anything.
        :rtype: None
        """
        self.recorded_cds_forms.append(form)

    def add_update_form(self, form: UpdateFormInfo) -> None:
        """
        Adds an Update Form to the list of Update forms.

        :param form: (UpdateFormInfo) - The Update Form to add.
        :type form: UpdateFormInfo
        :return: (None) - This method does not return anything.
        :rtype: None
        """
        self.update_forms.append(form)

    def add_recorded_update_form(self, form: UpdateFormInfo) -> None:
        """
        Adds a recorded Update Form to the list of recorded Update forms.

        :param form: (UpdateFormInfo) - The recorded Update Form to add.
        :type form: UpdateFormInfo
        :return: (None) - This method does not return anything.
        :rtype: None
        """
        self.recorded_update_forms.append(form)

    def add_class_form(self, form: ClassFormInfo) -> None:
        """
        Adds a Class Form to the list of Class forms.

        :param form: (ClassFormInfo) - The Class Form to add.
        :type form: ClassFormInfo
        :return: (None) - This method does not return anything.
        :rtype: None
        """
        self.class_forms.append(form)

    def add_recorded_class_form(self, form: ClassFormInfo) -> None:
        """
        Adds a recorded Class Form to the list of recorded Class forms.

        :param form: (ClassFormInfo) - The recorded Class Form to add.
        :type form: ClassFormInfo
        :return: (None) - This method does not return anything.
        :rtype: None
        """
        self.recorded_class_forms.append(form)

    def get_available_class_forms(self) -> list[ClassFormInfo]:
        """
        Returns a list of Class Forms that have not been previously retrieved or recorded

        :return: (list[ClassFormInfo]) - A list of Class Forms that are available to retrieve.
        :rtype: list[ClassFormInfo]
        """
        return [
            form for form in self.class_forms if form not in self.recorded_class_forms
        ]

    def get_available_cds_forms(self) -> list[CDSFormInfo]:
        """
        Returns a list of CDS Forms that have not been previously retrieved or recorded

        :return: (list[CDSFormInfo]) - A list of CDS Forms that are available to retrieve.
        :rtype: list[CDSFormInfo]
        """
        return [form for form in self.cds_forms if form not in self.recorded_cds_forms]

    def get_available_update_forms(self) -> list[UpdateFormInfo]:
        """
        Returns a list of Update Forms that have not been previously retrieved
        or recorded

        :return: (list[UpdateFormInfo]) - A list of Update Forms that are available to retrieve.
        :rtype: list[UpdateFormInfo]
        """
        return [
            form for form in self.update_forms if form not in self.recorded_update_forms
        ]

    def match_info_by_date(self, class_date: str) -> ClassFormInfo:
        """
        Returns a Class Form that matches the given date.

        :param class_date: (str) - The date to match the Class Form to.
        :type class_date: str
        :return: (ClassFormInfo) - The Class Form that matches the given date.
        :rtype: ClassFormInfo
        """
        return [form for form in self.class_forms if form.date == class_date][0]

    def record_assessment(self) -> None:
        """
        Records the assessment by checking the existence of the Assessment.xlsx file
        and updates the `assessment` attribute with a tuple containing the existence
        status and the file path.

        :return: (None) - This method does not return anything.
        :rtype: None
        """
        path: Path = paths.get_paths_excel()["Assessment"]
        self.assessment = (path.exists(), path)

    def record_attendance(self) -> None:
        """
        Records the attendance by checking the existence of the Attendance.xlsx file
        and updates the `attendance` attribute with a tuple containing the existence
        status and the file path.

        :return: (None) - This method does not return anything.
        :rtype: None
        """
        path = paths.get_paths_excel()["Attendance"]
        self.attendance = (path.exists(), path)

    def record_project(self) -> None:
        """
        Records the project by checking the existence of the Project.xlsx file
        and updates the `project` attribute with a tuple containing the existence
        status and the file path.

        :return: (None) - This method does not return anything.
        :rtype: None
        """
        path = paths.get_paths_excel()["Project"]
        self.project = (path.exists(), path)

    def record_result(self) -> None:
        """
        Records the result by checking the existence of the Result.xlsx file
        and updates the `result` attribute with a tuple containing the existence
        status and the file path.

        :return: (None) - This method does not return anything.
        :rtype: None
        """
        path = paths.get_paths_excel()["Result"]
        self.result = (path.exists(), path)

    def record_merit(self) -> None:
        """
        Records the merit by checking the existence of the Merit.xlsx file
        and updates the `merit` attribute with a tuple containing the existence
        status and the file path.

        :return: (None) - This method does not return anything.
        :rtype: None
        """
        if self.cohort is None:
            raise HistoryError("Cohort is not set")

        path = paths.get_merit_path(self.cohort)
        self.merit = (path.exists(), path)

    @property
    def has_collated_attendance(self) -> bool:
        """
        Property indicating whether the attendance records have been collated.

        :return: (bool) - A boolean indicating whether the attendance records have been collated.
        :rtype: bool
        """
        return self.attendance[0]

    @property
    def has_collated_assessment(self) -> bool:
        """
        Property indicating whether the assessment scores have been collated.

        :return: (bool) - A boolean indicating whether the assessment scores have been collated.
        :rtype: bool
        """
        return self.assessment[0]

    @property
    def has_collated_project(self) -> bool:
        """
        Property indicating whether the project scores have been collated.

        :return: (bool) - A boolean indicating whether the project scores have been collated.
        :rtype: bool
        """
        return self.project[0]

    @property
    def has_collated_merit(self) -> bool:
        """
        Property indicating whether the merit scores have been collated.

        :return: (bool) - A boolean indicating whether the merit scores have been collated.
        :rtype: bool
        """
        return self.merit[0]

    @property
    def has_collated_all(self) -> bool:
        """
        Property indicating whether all necessary records (attendance, assessment, and project)
        have been collated.

        :return: (bool) - A boolean indicating whether all necessary records have been collated.
        :rtype: bool
        """
        return (
            self.has_collated_attendance
            and self.has_collated_assessment
            and self.has_collated_project
        )

    @property
    def has_collated_result(self) -> bool:
        """
        Property indicating whether the result has been collated.

        :return: (bool) - A boolean indicating whether the result has been collated.
        :rtype: bool
        """
        return self.result[0]

    def get_unheld_classes(self) -> list[datetime]:
        """
        Returns a list of unheld classes i.e., classes that are not part of the held_classes list.

        :return: (list[datetime]) - A list of datetime objects representing the unheld classes.
        :rtype: list[datetime]
        """
        return [date for date in self.dates if date not in self.held_classes]

    def get_unmarked_classes(self) -> list[datetime]:
        """
        Returns a list of unmarked classes i.e., classes that are held and have attendance generated
        for them but have not had their attendances marked.

        :return: (list[datetime]) - A list of datetime objects representing the unmarked classes.
        :rtype: list[datetime]
        """
        return [date for date in self.held_classes if date not in self.marked_classes]
