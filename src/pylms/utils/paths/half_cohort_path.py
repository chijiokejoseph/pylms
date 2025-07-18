from pathlib import Path

from pylms.utils.paths.path_fns import get_excel_path


def get_cohort_path(cohort_no: int) -> Path:
    return get_excel_path() / f"Python Beginners Cohort {cohort_no} Attendance.xlsx"
