from pylms.cli.errors import ForcedExitError


def input_fn(msg: str) -> str:
    """
    Prompt the user for input with an option to forcefully exit the operation.

    :param msg: (str) - The message to display to the user.
    :type msg: str

    :return: (str) - The user's input if not a forced exit command.
    :rtype: str

    :raises ForcedExitError: If the user inputs 'quit', 'exit', or 'q' to exit the operation.
    """
    # Append exit instructions to the prompt message
    msg += "\n[To forcefully exit the operation enter 'quit', 'exit' or 'q']: "
    # Get user input
    user_input: str = input(msg)
    # Check if user wants to forcefully exit
    if user_input in ["quit", "exit", "q"]:
        raise ForcedExitError("You quit the operation")
    else:
        # Return the user input if not exiting
        return user_input
