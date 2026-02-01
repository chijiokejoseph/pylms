from ..cli import input_num
from ..errors import Result


def input_marks_req(msg: str, min: int = 1, max: int = 100) -> Result[int]:
    """Prompt user for marks requirement within specified range.
    
    Validates that input is between min and max values (inclusive).
    
    Args:
        msg (str): Prompt message to display to user.
        min (int): Minimum allowed value. Defaults to 1.
        max (int): Maximum allowed value. Defaults to 100.
        
    Returns:
        Result[int]: Success with validated mark requirement or error.
    """
    return input_num(
        msg,
        1,
        test_fn=lambda x: min <= x <= max,
        diagnosis=f"The entered number must be between {min} and {max}",
    )


def input_ratio_req(msg: str) -> Result[float]:
    """Prompt user for ratio requirement between 0 and 1.
    
    Validates that input is a valid ratio (0.0 to 1.0 inclusive).
    
    Args:
        msg (str): Prompt message to display to user.
        
    Returns:
        Result[float]: Success with validated ratio requirement or error.
    """
    return input_num(
        msg,
        1.0,
        test_fn=lambda x: 0 <= x <= 1,
        diagnosis="The entered number must be between 0 and 1",
    )
