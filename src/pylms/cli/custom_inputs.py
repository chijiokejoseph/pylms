from typing import Callable, cast, overload

from pylms.cli.input_with_quit import input_fn
from pylms.errors import LMSError, Result, eprint


@overload
def input_num(  # pyright: ignore[reportOverlappingOverload]
    prompt: str,
    sample: int,
    test_fn: Callable[[int], bool] = lambda x: True,
    diagnosis: str | None = None,
    trials: int = 3,
) -> Result[int]: ...


@overload
def input_num(
    prompt: str,
    sample: float,
    test_fn: Callable[[float], bool] = lambda x: True,
    diagnosis: str | None = None,
    trials: int = 3,
) -> Result[float]: ...


def input_num(
    prompt: str,
    sample: int | float,
    test_fn: Callable[[int], bool] | Callable[[float], bool] = lambda x: True,
    diagnosis: str | None = None,
    trials: int = 3,
) -> Result[int] | Result[float]:
    """
    Prompts the user to enter a number and validates the input.
    This function repeatedly prompts the user for input, attempting to parse the input as either a float or an integer
    based on the specified return type (`rtype`). It validates the parsed input using a custom test function (`test_fn`).
    If the input is valid, it returns the parsed number. If the input is invalid or cannot be parsed, it informs the user and retries for a specified number of trials (`trials`). If all trials are exhausted, a bad result (`Result`) is returned.

    :param msg: (str) - The message to display to the user when prompting for input.

    :param sample: (int | float) - A sample that denotes if the returned number should be int or float

    :param test_fn: (Callable[[float], bool]) - A function to test the validity of the parsed input. Defaults to a function that returns True for any input.

    :param diagnosis: (str | None) - An optional message to display if the parsed input fails the test function.

    :param trials: (int) - The number of attempts to allow the user to input a valid number before raising an error. Defaults to 3.

    :return: (Result[float]) - A result containing the validated and parsed number input by the user.
    :rtype: Result[float]
    """

    _ = sample
    # repeat loop until the user enters a valid input and triggers an early return
    for _ in range(trials):
        # get user input
        result: Result[str] = input_fn(prompt)
        if result.is_err():
            return result.propagate()

        response: str = result.unwrap().lower().strip()
        # attempt to convert user input to number
        try:
            if "." in response:
                selection = float(response)
                test_fn = cast(Callable[[float], bool], test_fn)
                if test_fn(selection):
                    print()
                    return Result.ok(selection)
                elif diagnosis is None:
                    eprint(f"{selection} is a number but not a valid value\n")
                else:
                    eprint(f"You have selected {selection}. {diagnosis}\n")
            else:
                selection = int(response)
                test_fn = cast(Callable[[int], bool], test_fn)
                if test_fn(selection):
                    print()
                    return Result.ok(selection)
                elif diagnosis is None:
                    eprint(f"{selection} is a number but not a valid value\n")
                else:
                    eprint(f"You have selected {selection}. {diagnosis}\n")
            # validate `selection` the num result of converting the user input to  number

        except ValueError:
            # print warning message if the user input is not parsable to a number
            eprint(f"{response} is not a valid number\n")

    # Forcefully exit the program by raising an InvalidInputError if the loop is exhausted and no valid input has been entered
    return Result.err(
        LMSError(
            f"You've entered an invalid response {trials} times. Please restart the program.",
        )
    )


def input_str(
    msg: str,
    test_fn: Callable[[str], bool] = lambda x: True,
    diagnosis: str | None = None,
    trials: int = 3,
    lower_case: bool = True,
) -> Result[str]:
    # repeat execution until the user enters a valid str response or loops is exhausted
    """
    Prompts the user to enter a str and validates the input.
    This function repeatedly prompts the user for input, attempting to validate the input using a custom test function (`test_fn`).
    If the input is valid, it returns the validated str. If the input is invalid or cannot be parsed, it informs the user
    and retries for a specified number of trials (`trials`). If all attempts are exhausted without a valid input, it returns a bad result (`Result`).

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

    :return: (Result[str]) - A result containing the validated and parsed str input by the user.
    :rtype: Result[str]

    """
    for _ in range(trials):
        # get input from the user
        result: Result[str] = input_fn(msg)
        if result.is_err():
            error = result.unwrap_err()
            return Result[str].err(error)
        response: str = result.unwrap().strip()
        if lower_case:
            response = response.lower()
        # validate input with `test_fn`
        if test_fn(response):
            # return early if input is valid
            print()
            return Result[str].ok(response)
        else:
            # print message on invalid input from the user
            # print default message if `diagnosis` is None
            # else print `diagnosis`
            if diagnosis is None:
                eprint("You have entered an invalid response\n")
            else:
                eprint(f"You have entered {response}. {diagnosis}\n")
    return Result[str].err(
        LMSError(
            f"You've entered an invalid response {trials} times. Please restart the program.",
        )
    )
