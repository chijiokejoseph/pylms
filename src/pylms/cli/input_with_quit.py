from pylms.cli.errors import ForcedExitError


def input_fn(msg: str) -> str:
    msg += "\n[To forcefully exit the operation enter 'quit', 'exit' or 'q']: "
    user_input: str = input(msg)
    if user_input in ["quit", "exit", "q"]:
        raise ForcedExitError("You quit the operation")
    else:
        return user_input
