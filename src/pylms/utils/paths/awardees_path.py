from pathlib import Path

from pylms.config import read_course_name
from pylms.utils.paths.path_fns import get_excel_path


def get_fast_track_path(cohort_num: int) -> Path:
    return (
        get_excel_path()
        / f"{read_course_name()} Cohort {cohort_num} Fast Track Awardees.xlsx"
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
