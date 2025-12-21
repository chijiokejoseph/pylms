from ..errors import ForcedExitError, Result, eprint


def input_fn(msg: str) -> Result[str]:
    """Prompt the user for input with an option to forcefully exit the operation.

    Presents the provided prompt to the user and returns the entered string
    wrapped in a `Result.ok`. If the user types one of the force-exit commands
    ('quit', 'exit', or 'q'), a message is printed and the function returns
    `Result.err` containing a `ForcedExitError`.

    Args:
        msg (str): The message to display to the user.

    Returns:
        Result[str]: `Result.ok` with the user's input, or `Result.err` with a
            `ForcedExitError` when the user requests a forced exit.
    """

    # Append exit instructions to the prompt message
    msg += "\n[To forcefully exit the operation enter 'quit', 'exit' or 'q']: "

    # Get user input
    user_input: str = input(msg)

    # Check if user wants to forcefully exit
    if user_input in ["quit", "exit", "q"]:
        msg = "You quit the operation"
        eprint(msg)
        return Result.err(ForcedExitError(msg))
    else:
        # Return the user input if not exiting
        return Result.ok(user_input)
