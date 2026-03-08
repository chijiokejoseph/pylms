from typing import NamedTuple

from ..errors import ForcedExitError, Result, eprint
from ..info import print_info
from ..result_utils import input_marks_req, input_ratio_req


class CollateReq(NamedTuple):
    """Requirements for result collation.
    
    Contains pass mark and ratio requirements for assessment and project components.
    
    Attributes:
        pass_mark (float): Pass mark for the course (1-100).
        assessment_ratio (float): Assessment weight in final grade (0-1).
        project_ratio (float): Project weight in final grade (0-1).
    """
    pass_mark: float
    assessment_ratio: float
    project_ratio: float


def input_collate_req() -> Result[CollateReq]:
    """Prompt user for pass mark and component ratios.
    
    Collects pass mark (1-100) and assessment/project ratios (0-1) from user.
    Validates that ratios sum to 1.0 within tolerance.
    
    Loops until successful input or ForcedExitError.
    
    Returns:
        Result[CollateReq]: Success with collation requirements or ForcedExitError.
    """
    while True:
        # Prompt for pass mark
        passmark = input_marks_req("Enter the Pass Mark [1 - 100]: ")
        if passmark.is_err():
            err = passmark.unwrap_err()
            if isinstance(err, ForcedExitError):
                return passmark.propagate()
            passmark.print_if_err()
            continue
        passmark_val = passmark.unwrap()

        # Inform user about ratio inputs
        print_info(
            "You will enter the values for the assessment and project ratios. Please ensure both values add up to 1.\n"
        )

        # Prompt for assessment ratio
        assessment_ratio = input_ratio_req("Enter the Assessment Ratio [0 - 1]: ")
        if assessment_ratio.is_err():
            err = assessment_ratio.unwrap_err()
            if isinstance(err, ForcedExitError):
                return assessment_ratio.propagate()
            assessment_ratio.print_if_err()
            continue
        assessment_ratio_val = assessment_ratio.unwrap()

        # Prompt for project ratio
        project_ratio = input_ratio_req("Enter the Project Ratio [0 - 1]: ")
        if project_ratio.is_err():
            err = project_ratio.unwrap_err()
            if isinstance(err, ForcedExitError):
                return project_ratio.propagate()
            project_ratio.print_if_err()
            continue
        project_ratio_val = project_ratio.unwrap()

        # Validate ratios sum to 1
        diff = abs(1 - (assessment_ratio_val + project_ratio_val))
        if diff >= 1e-2:
            eprint(f"Assessment ratio {assessment_ratio_val} and Project Ratio {project_ratio_val} do not add up to 1.")
            continue

        return Result.ok(CollateReq(passmark_val, assessment_ratio_val, project_ratio_val))
