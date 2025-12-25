from pathlib import Path

from pylms.errors import Result

from ..config import read_course_name
from .path_fns import get_excel_path


def get_fast_track_path(cohort_num: int) -> Result[Path]:
    course_name = read_course_name()
    if course_name.is_err():
        return course_name.propagate()
    course_name = course_name.unwrap()

    value = (
        get_excel_path() / f"Cohort {cohort_num} {course_name} Fast Track Awardees.xlsx"
    )

    return Result.ok(value)


def get_merit_path(cohort_num: int) -> Result[Path]:
    course_name = read_course_name()
    if course_name.is_err():
        return course_name.propagate()
    course_name = course_name.unwrap()

    value = get_excel_path() / f"Cohort {cohort_num} {course_name} Merit Awardees.xlsx"
    return Result.ok(value)


def get_merged_path(cohort_num: int) -> Result[Path]:
    course_name = read_course_name()
    if course_name.is_err():
        return course_name.propagate()
    course_name = course_name.unwrap()

    value = (
        get_excel_path()
        / f"Cohort {cohort_num} {read_course_name()} Awardees Total.xlsx"
    )
    return Result.ok(value)
