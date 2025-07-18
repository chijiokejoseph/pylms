from pathlib import Path

from pylms.utils.paths.path_fns import get_excel_path


def get_list_path(cohort_num: int) -> Path:
    return get_excel_path() / f"Python Beginners Cohort {cohort_num} Records.xlsx"