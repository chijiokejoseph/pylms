from datetime import datetime
from pathlib import Path

from ..models import CDSFormInfo, ClassFormInfo, UpdateFormInfo


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

        group (tuple[bool, int]): A tuple containing a boolean indicating whether the groups have been created and the number of groups that was assigned.

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
        self.group: tuple[bool, int] = (False, 0)
        self._updated: bool = False

    @property
    def updated(self) -> bool:
        return self._updated

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

    @property
    def has_group(self) -> bool:
        """
        Returns True if the students have been grouped. False if not

        :return: (bool) - indicates if the students have been grouped for their projects or not
        :rtype: bool
        """

        return self.group[0]
