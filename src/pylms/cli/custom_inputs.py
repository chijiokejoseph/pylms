from typing import Callable, cast, overload

from ..errors import Result, eprint
from .input_with_quit import input_fn


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
    """Prompt the user for a numeric input and validate the response.

    This function repeatedly prompts the user and attempts to parse the entered
    text as either an integer or a float depending on the input. The parsed
    value is validated with `test_fn`. On success, the parsed number is
    returned wrapped in a `Result.ok`. If the user fails to provide valid
    input within `trials` attempts, a `Result.err` is returned.

    Args:
        prompt (str): The prompt message to display to the user.
        sample (int | float): Example value indicating whether an int or float
            is expected.
        test_fn (Callable[[int], bool] | Callable[[float], bool]): Validation
            callable that returns True for acceptable values.
        diagnosis (str | None): Optional diagnostic message shown when the
            parsed value fails `test_fn`.
        trials (int): Number of attempts allowed before returning an error.

    Returns:
        Result[int] | Result[float]: Ok containing the parsed numeric value
            (int or float) when validation succeeds, or an Err when attempts
            are exhausted or the interactive prompt fails.
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
        f"You've entered an invalid response {trials} times. Please restart the program.",
    )


def input_str(
    msg: str,
    test_fn: Callable[[str], bool] = lambda x: True,
    diagnosis: str | None = None,
    trials: int = 3,
    lower_case: bool = True,
) -> Result[str]:
    # repeat execution until the user enters a valid str response or loops is exhausted
    """Prompt the user for a validated string input.

    The helper prompts the user with `msg`, optionally lower-cases the
    response, and validates it with `test_fn`. When validation succeeds the
    function returns the string inside `Result.ok`. If the prompt fails or
    the user exhausts `trials` attempts, an error `Result` is returned.

    Args:
        msg (str): Prompt message to present to the user.
        test_fn (Callable[[str], bool]): Callable used to validate the input.
            Should return True when the input is acceptable.
        diagnosis (str | None): Optional diagnostic message printed when the
            input fails `test_fn`.
        trials (int): Number of attempts to allow before returning an error.
        lower_case (bool): If True the user's response is lower-cased before
            validation and return; otherwise the original casing is preserved.

    Returns:
        Result[str]: Ok with the validated string when successful, or Err
            containing a diagnostic message when validation or prompting fails.
    """
    for _ in range(trials):
        # get input from the user
        result: Result[str] = input_fn(msg)
        if result.is_err():
            return result.propagate()

        response: str = result.unwrap().strip()

        if lower_case:
            response = response.lower()

        # validate input with `test_fn`
        if test_fn(response):
            # return early if input is valid
            print()
            return Result.ok(response)
        else:
            # print message on invalid input from the user
            # print default message if `diagnosis` is None
            # else print `diagnosis`
            if diagnosis is None:
                eprint("You have entered an invalid response\n")
            else:
                eprint(f"You have entered {response}. {diagnosis}\n")

    return Result.err(
        f"You've entered an invalid response {trials} times. Please restart the program.",
    )
