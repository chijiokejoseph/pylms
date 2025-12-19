from ..constants import ASSESSMENT, ATTENDANCE, PROJECT, RESULT


def _det_total_col(title: str, total: int) -> str:
    return title + f" [{total}]"


def _det_overall_col(title: str, percent: float | None = None) -> str:
    overall: float = 100 if percent is None else percent
    overall = round(overall, 0)
    if 0 <= overall <= 1:
        overall *= 100
    return title + f" [{overall:.0f}%]"


def _det_score_col(title: str) -> str:
    return title + " [100%]"


def _det_req_col(title: str) -> str:
    return title + " Req"


def det_attendance_total_col(total: int) -> str:
    return _det_total_col(ATTENDANCE, total)


def det_attendance_score_col() -> str:
    return _det_score_col(ATTENDANCE)


def det_attendance_req_col() -> str:
    return _det_req_col(ATTENDANCE)


def det_assessment_score_col() -> str:
    return _det_score_col(ASSESSMENT)


def det_assessment_req_col() -> str:
    return _det_req_col(ASSESSMENT)


def det_assessment_overall_col(assessment_ratio: float) -> str:
    if 0 <= assessment_ratio <= 1:
        assessment_ratio *= 100
    return _det_overall_col(ASSESSMENT, assessment_ratio)


def det_project_score_col() -> str:
    return _det_score_col(PROJECT)


def det_project_overall_col(project_ratio: float) -> str:
    if 0 <= project_ratio <= 1:
        project_ratio *= 100
    return _det_overall_col(PROJECT, project_ratio)


def det_result_col() -> str:
    return _det_score_col(RESULT)


def det_passmark_col() -> str:
    return _det_req_col(RESULT)


def list_print(input_list: list[str]) -> str:
    output: str = "[\n"
    for item in input_list:
        output += f"\t{item}\n"
    output += "]\n"
    return output
