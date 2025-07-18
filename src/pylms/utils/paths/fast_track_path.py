from pathlib import Path

from pylms.constants import COURSE_NAME
from pylms.utils.paths.path_fns import get_excel_path


def get_fast_track_path(cohort_num: int) -> Path:
    return (
        get_excel_path() / f"{COURSE_NAME} Cohort {cohort_num} Fast Track Awardees.xlsx"
    )
