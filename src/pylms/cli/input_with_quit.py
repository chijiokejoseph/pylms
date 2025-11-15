from pylms.errors import ForcedExitError, Result, eprint


def input_fn(msg: str) -> Result[str]:
    """
    Prompt the user for input with an option to forcefully exit the operation.

    :param msg: (str) - The message to display to the user.
    :type msg: str

    :return: (Result[str]) - The user's input if not a forced exit command.
    :rtype: Result

    :raises ForcedExitError: If the user inputs 'quit', 'exit', or 'q' to exit the operation.
    """
    # Append exit instructions to the prompt message
    msg += "\n[To forcefully exit the operation enter 'quit', 'exit' or 'q']: "
    # Get user input
    user_input: str = input(msg)
    # Check if user wants to forcefully exit
    if user_input in ["quit", "exit", "q"]:
        msg = "You quit the operation"
        eprint(msg)
        return Result[str].err(ForcedExitError(msg))
    else:
        # Return the user input if not exiting
        return Result[str].ok(user_input)
