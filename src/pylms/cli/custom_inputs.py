from typing import Callable, Literal

from pylms.cli.errors import InvalidInputError
from pylms.cli.input_with_quit import input_fn

type T = float | int


def input_num(
    msg: str,
    rtype: Literal["float", "int"],
    test_fn: Callable[[T], bool] = lambda x: True,
    diagnosis: str | None = None,
    trials: int = 3,
) -> T:
    
    """
    Prompts the user to enter a number and validates the input.
    This function repeatedly prompts the user for input, attempting to parse the input as either a float or an integer
    based on the specified return type (`rtype`). It validates the parsed input using a custom test function (`test_fn`).
    If the input is valid, it returns the parsed number. If the input is invalid or cannot be parsed, it informs the user
    and retries for a specified number of trials (`trials`). If all attempts are exhausted without a valid input, it raises
    an `InvalidInputError`.
    
        `T` = float | int

    :param msg: (str) - The message to display to the user when prompting for input.
    :param rtype: (Literal["float", "int"]) - The desired return type of the input, either "float" or "int".
    :param test_fn: (Callable[[T], bool]) - A function to test the validity of the parsed input. Defaults to a function that returns True for any input.
    :param diagnosis: (str | None) - An optional message to display if the parsed input fails the test function.
    :param trials: (int) - The number of attempts to allow the user to input a valid number before raising an error. Defaults to 3.

    :return: (T) - The validated and parsed number input by the user.

    :raises InvalidInputError: If the user fails to input a valid number within the allowed number of trials.
    """

    converter = float if rtype == "float" else int
    # repeat loop until the user enters a valid input and triggers an early return
    for _ in range(trials):
        # get user input
        response: str = input_fn(msg).lower().strip()

        # attempt to convert user input to number
        try:
            selection: T = converter(response)
            # validate `selection` the num result of converting the user input to  number
            if test_fn(selection):
                print()
                return selection
            elif diagnosis is None:
                print(f"{selection} is a number but not a valid value")
            else:
                print(f"You have selected {selection}. {diagnosis}")
        except ValueError:
            # print warning message if the user input is not parsable to a number
            print(f"{response} is not a valid number")

    # Forcefully exit the program by raising an InvalidInputError if the loop is exhausted and no valid input has been entered
    raise InvalidInputError(
        f"You've entered an invalid response {trials} times. Please restart the program.",
        parsing_to="int",
        validation_fn=test_fn,
    )


def input_str(
    msg: str,
    test_fn: Callable[[str], bool] = lambda x: True,
    diagnosis: str | None = None,
    trials: int = 3,
    lower_case: bool = True,
) -> str:
    
    # repeat execution until the user enters a valid str response or loops is exhausted
    """
    Prompts the user to enter a str and validates the input.
    This function repeatedly prompts the user for input, attempting to validate the input using a custom test function (`test_fn`).
    If the input is valid, it returns the validated str. If the input is invalid or cannot be parsed, it informs the user
    and retries for a specified number of trials (`trials`). If all attempts are exhausted without a valid input, it raises
    an `InvalidInputError`.
    
    :param msg: (str) - The message to display to the user when prompting for input.
    :type msg: str
    :param test_fn: (Callable[[str], bool]) - A function to test the validity of the parsed input. Defaults to a function that returns True for any input.
    :type test_fn: Callable[[str], bool]
    :param diagnosis: (str | None) - An optional message to display if the parsed input fails the test function.
    :type diagnosis: str | None
    :param trials: (int) - The number of attempts to allow the user to input a valid str before raising an error. Defaults to 3.
    :type trials: int
    :param lower_case: (bool) - Whether to convert the input to lower case before validating and returning. Defaults to True.
    :type lower_case: bool
    
    :return: (str) - The validated and parsed str input by the user.
    :rtype: str
    
    :raises InvalidInputError: If the user fails to input a valid str within the allowed number of trials.
    """
    for trial in range(trials):
        # get input from the user
        response: str = input_fn(msg).strip()
        if lower_case:
            response = response.lower()
        # validate input with `test_fn`
        if test_fn(response):
            # return early if input is valid
            print()
            return response
        else:
            # print message on invalid input from the user
            # print default message if `diagnosis` is None
            # else print `diagnosis`
            if diagnosis is None:
                print("You have entered an invalid response")
            else:
                print(f"You have entered {response}. {diagnosis}")
    raise InvalidInputError(
        f"You've entered an invalid response {trials} times. Please restart the program.",
        parsing_to="str",
        validation_fn=test_fn,
    )
