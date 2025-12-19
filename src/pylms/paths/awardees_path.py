from pathlib import Path

from ..config import read_course_name
from .path_fns import get_excel_path


def get_fast_track_path(cohort_num: int) -> Path:
    return (
        get_excel_path()
        / f"Cohort {cohort_num} {read_course_name()} Fast Track Awardees.xlsx"
    )


def get_merit_path(cohort_num: int) -> Path:
    return (
        get_excel_path()
        / f"Cohort {cohort_num} {read_course_name()} Merit Awardees.xlsx"
    )


def get_merged_path(cohort_num: int) -> Path:
    return (
        get_excel_path()
        / f"Cohort {cohort_num} {read_course_name()} Awardees Total.xlsx"
    )
