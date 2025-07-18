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
    a custom input function for receiving numbers from the user. The function works using a for loop that exits abnormally when the user enters a valid input using an early return else the function continues to repeat its process until the loop is exhausted, after which it forcefully exits. The number of loops is controlled by the argument to the `trials` parameter.

    type T = int | float i.e., T is just an alias for a Union of int and float.

    The function operates in the following stages:

        - The function outputs a prompt to the user based on the argument passed to the `msg` parameter of the function.

        - The function then attempts to convert the response to an int or float based on the value passed to `rtype`. If the conversion is not successful due to an invalid string literal entered by the user, it prints a warning and then skips the rest of the loop

        - If the conversion is successful, the function attempts to validate the converted int or float using the argument to `test_fn`.

            - If the validation fails, a message is printed out. An additional diagnostic message can be printed out if `diagnosis` is not None. After which the rest of the loop is skipped.

            - Else, the function returns the converted int or float.

    :param msg: (str): the message to be used as a prompt to the user
    :type msg: str

    :param rtype: (Literal["int", "float"]): the type of the number to be returned i.e., either int or float.
    :type rtype: Literal["int", "float"]

    :param test_fn: (Callable[[T], bool], optional): the function to be used to test the validity of the converted int or float. It defaults to `lambda x: True`.
    :type test_fn: Callable[[T], bool]

    :param diagnosis: (str | None, optional): A special diagnostic message to be printed to the user if the validation of `test_fn` should fail. It defaults to None.
    :type diagnosis: str | None

    :param trials: (int, optional): The maximum number of times to prompt the user and validate his response before raising an `InvalidInputError` Error if no valid input is entered before the loop is exhausted. It defaults to 3
    :type trials: int

    :return: the number which this function is defined to get from the user.
    :rtype: T
    :raises: InvalidInputError
    """
    converter = float if rtype == "float" else int
    # repeat loop until the user enters a valid input and triggers an early return
    for trial in range(trials):
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
    """
    A custom input function for receiving strings from the user. The function works using a for loop that exits abnormally when the user enters a valid input using an early return, else the function continues to repeat its process until the loop is exhausted after which it forcefully exits. The number of loops is controlled by the argument to the `trials` parameter.

    The function operates in the following stages:

        - The function outputs a prompt to the user based on the argument passed to the `msg` parameter of the function.

        - The function attempts to validate the response entered by the user using the argument to `test_fn`.

            - If the validation fails, a message is printed out. An additional diagnostic message can be printed out if `diagnosis` is not None. After which the rest of the loop is skipped.

            - Else, the function returns the user's response.

    :param msg: ( str ): the message to be used as a prompt to the user
    :type msg: str
    :param test_fn: ( Callable[[str], bool], optional ): the function to be used to test the validity of the user's input. It defaults to `lambda x: True`.
    :type test_fn: Callable[[str], bool]
    :param diagnosis: ( str | None, optional ): A special diagnostic message to be printed to the user if the validation of `test_fn` should fail. It defaults to None.
    :type diagnosis: str | None
    :param trials: ( int, optional ): The maximum number of times to prompt the user and validate his response before raising an `InvalidInputError` if no valid input is entered before the loop is exhausted. It defaults to 3
    :type trials: int
    :param lower_case: ( bool, optional ): A boolean that indicates if the input should be lowercased or not. It defaults to True.
    :type lower_case: bool

    :return: the string input which this function is defined to get from the user.
    :rtype: str
    :raises: InvalidInputError
    """
    # repeat execution until the user enters a valid str response or loops is exhausted
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
