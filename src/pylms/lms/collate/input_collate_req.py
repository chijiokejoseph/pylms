from typing import NamedTuple, cast

from pylms.cli import input_num
from pylms.lms.collate.errors import GradingRatioErr


class CollateReq(NamedTuple):
    pass_mark: float
    attendance_req: float
    assessment_req: float
    assessment_ratio: float
    project_ratio: float


def input_collate_req() -> CollateReq:
    temp = input_num(
        "Enter the Pass Mark [1 - 100]: ",
        "int",
        test_fn=lambda x: 1 <= x <= 100,
        diagnosis="The entered number must be between 1 and 100",
    )
    pass_mark: int = cast(int, temp)
    temp = input_num(
        "Enter the Attendance Requirement [1 - 100]: ",
        "int",
        test_fn=lambda x: 1 <= x <= 100,
        diagnosis="The entered number must be between 1 and 100",
    )
    attendance_req: float = float(temp)
    temp = input_num(
        "Enter the Assessment Ratio [0 - 1]: ",
        "float",
        test_fn=lambda x: 0 <= x <= 1,
        diagnosis="The number must be between 0 and 1",
    )
    assessment_ratio: float = float(temp)
    assessment_total: float = assessment_ratio * 100
    assessment_total = round(assessment_total, 2)
    temp = input_num(
        f"Enter the Assessment Requirement [1 - {assessment_total}]: ",
        "int",
        test_fn=lambda x: 1 <= x <= assessment_total,
        diagnosis=f"The entered number must be between 1 and {assessment_total}",
    )
    assessment_req: float = float(temp)
    temp = input_num(
        "Enter the Project Ratio [0 - 1]: ",
        "float",
        test_fn=lambda x: 0 <= x <= 1,
        diagnosis="The number must be between 0 and 1",
    )
    project_ratio: float = float(temp)
    diff: float = abs(1 - (assessment_ratio + project_ratio))
    if diff >= 1e-2:
        raise GradingRatioErr(
            f"Assessment ratio {assessment_ratio} and Project Ratio {project_ratio} do not add up to 1."
        )
    return CollateReq(
        pass_mark, attendance_req, assessment_req, assessment_ratio, project_ratio
    )
