from ..constants import ASSESSMENT, ATTENDANCE, PROJECT, RESULT


def _det_total_col(title: str, total: int) -> str:
    """Generate total column name with count.
    
    Args:
        title (str): Base column title.
        total (int): Total count value.
        
    Returns:
        str: Formatted column name with total.
    """
    return title + f" [{total}]"


def _det_overall_col(title: str, percent: float | None = None) -> str:
    """Generate overall column name with percentage.
    
    Args:
        title (str): Base column title.
        percent (float | None): Percentage value, defaults to 100.
        
    Returns:
        str: Formatted column name with percentage.
    """
    overall = 100 if percent is None else percent
    overall = round(overall, 0)
    if 0 <= overall <= 1:
        overall *= 100
    return title + f" [{overall:.0f}%]"


def _det_score_col(title: str) -> str:
    """Generate score column name with 100% indicator.
    
    Args:
        title (str): Base column title.
        
    Returns:
        str: Formatted score column name.
    """
    return title + " [100%]"


def _det_req_col(title: str) -> str:
    """Generate requirement column name.
    
    Args:
        title (str): Base column title.
        
    Returns:
        str: Formatted requirement column name.
    """
    return title + " Req"


def det_attendance_total_col(total: int) -> str:
    """Generate attendance total column name.
    
    Args:
        total (int): Total attendance count.
        
    Returns:
        str: Formatted attendance total column name.
    """
    return _det_total_col(ATTENDANCE, total)


def det_attendance_score_col() -> str:
    """Generate attendance score column name.
    
    Returns:
        str: Formatted attendance score column name.
    """
    return _det_score_col(ATTENDANCE)


def det_attendance_req_col() -> str:
    """Generate attendance requirement column name.
    
    Returns:
        str: Formatted attendance requirement column name.
    """
    return _det_req_col(ATTENDANCE)


def det_assessment_score_col() -> str:
    """Generate assessment score column name.
    
    Returns:
        str: Formatted assessment score column name.
    """
    return _det_score_col(ASSESSMENT)


def det_assessment_req_col() -> str:
    """Generate assessment requirement column name.
    
    Returns:
        str: Formatted assessment requirement column name.
    """
    return _det_req_col(ASSESSMENT)


def det_assessment_overall_col(assessment_ratio: float) -> str:
    """Generate assessment overall column name with ratio.
    
    Args:
        assessment_ratio (float): Assessment weight ratio.
        
    Returns:
        str: Formatted assessment overall column name.
    """
    if 0 <= assessment_ratio <= 1:
        assessment_ratio *= 100
    return _det_overall_col(ASSESSMENT, assessment_ratio)


def det_project_score_col() -> str:
    """Generate project score column name.
    
    Returns:
        str: Formatted project score column name.
    """
    return _det_score_col(PROJECT)


def det_project_overall_col(project_ratio: float) -> str:
    """Generate project overall column name with ratio.
    
    Args:
        project_ratio (float): Project weight ratio.
        
    Returns:
        str: Formatted project overall column name.
    """
    if 0 <= project_ratio <= 1:
        project_ratio *= 100
    return _det_overall_col(PROJECT, project_ratio)


def det_result_col() -> str:
    """Generate result column name.
    
    Returns:
        str: Formatted result column name.
    """
    return _det_score_col(RESULT)


def det_passmark_col() -> str:
    """Generate passmark column name.
    
    Returns:
        str: Formatted passmark column name.
    """
    return _det_req_col(RESULT)


def list_print(input_list: list[str]) -> str:
    """Format list as indented string representation.
    
    Args:
        input_list (list[str]): List of strings to format.
        
    Returns:
        str: Formatted string with brackets and indentation.
    """
    output = "[\n"
    for item in input_list:
        output += f"\t{item}\n"
    output += "]\n"
    return output
