from ..cli import input_num
from ..errors import Result


def input_marks_req(msg: str, min: int = 1, max: int = 100) -> Result[int]:
    """
    Prompts the user to enter a number between 1 and 100 and validates the input.

    :param msg: the message to be used as a prompt to the user
    :type msg: str

    :param min: (int) - the minimum value allowed for the input. Defaults to 1.
    :type min: int

    :param max: (int) - the maximum value allowed for the input. Defaults to 100.
    :type max: int

    :return: the validated mark requirement
    :rtype: int
    """
    return input_num(
        msg,
        1,
        test_fn=lambda x: min <= x <= max,
        diagnosis=f"The entered number must be between {min} and {max}",
    )


def input_ratio_req(msg: str) -> Result[float]:
    """
    Prompts the user to enter a number between 0 and 1 and validates the input.

    :param msg: the message to be used as a prompt to the user
    :type msg: str

    :return: the validated ratio requirement
    :rtype: float
    """
    return input_num(
        msg,
        1.0,
        test_fn=lambda x: 0 <= x <= 1,
        diagnosis="The entered number must be between 0 and 1",
    )
