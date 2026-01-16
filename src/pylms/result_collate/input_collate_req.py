from typing import NamedTuple

from ..errors import Result, eprint
from ..info import print_info
from ..result_utils import input_marks_req, input_ratio_req


class CollateReq(NamedTuple):
    """
    A tuple of the pass mark, assessment ratio and project ratio.

    Attributes:
        pass_mark (float): The pass mark for the course.
        assessment_ratio (float): The ratio of the assessment to the course mark.
        project_ratio (float): The ratio of the project to the course mark.
    """

    pass_mark: float
    assessment_ratio: float
    project_ratio: float


def input_collate_req() -> Result[CollateReq]:
    """
    Prompts the user to input the pass mark, assessment ratio and project ratio.

    The function will first prompt the user to enter a pass mark between 1 and 100. It will then prompt the user to enter the assessment and project ratios. For the ratios, the user is expected to enter a number between 0 and 1. The function will then check if the two ratios entered add up to 1. If they do not, an exception of type GradingRatioErr will be raised.

    :return: (Result[CollateReq]) - A result containing the tuple of the pass mark and the two ratios.
    :rtype: Result[CollateReq]
    """
    # 1. prompt the user to enter a pass mark
    passmark = input_marks_req("Enter the Pass Mark [1 - 100]: ")
    if passmark.is_err():
        return passmark.propagate()
    passmark = passmark.unwrap()

    # 2. inform the user that the next inputs are ratios
    print_info(
        "You will enter the values for the assessment and project ratios. Please ensure both values add up to 1.\n"
    )

    # 3. prompt the user to enter the assessment ratio
    assessment_ratio = input_ratio_req("Enter the Assessment Ratio [0 - 1]: ")
    if assessment_ratio.is_err():
        return assessment_ratio.propagate()
    assessment_ratio = assessment_ratio.unwrap()

    # 4. prompt the user to enter the project ratio
    project_ratio = input_ratio_req("Enter the Project Ratio [0 - 1]: ")
    if project_ratio.is_err():
        return Result.err(project_ratio.unwrap_err())
    project_ratio = project_ratio.unwrap()

    # 5. check if the two ratios add up to 1
    diff: float = abs(1 - (assessment_ratio + project_ratio))
    if diff >= 1e-2:
        msg = f"Assessment ratio {assessment_ratio} and Project Ratio {project_ratio} do not add up to 1."
        eprint(msg)
        return Result.err(msg)

    # 6. return the pass mark and ratios as a tuple
    return Result.ok(CollateReq(passmark, assessment_ratio, project_ratio))
