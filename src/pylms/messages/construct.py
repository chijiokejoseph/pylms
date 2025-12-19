from ..cli import input_option, input_str
from ..errors import Result


def construct_msg(prompt: str | None = None) -> Result[str]:
    """
    Constructs a multi-line message by prompting the user to enter lines one at a time.

    The user is repeatedly asked to input a new line, which is appended to the message.
    Input ends when the user enters 'DONE' (case-insensitive).

    :return: The constructed multi-line message as a string.
    :rtype: str
    """
    message: str = ""  # Initialize the message as an empty string

    confirm_menu: list[str] = [
        "Continue Adding Lines",
        "Clear Message and Restart",
        "Proceed with Message",
    ]

    prompt_str: str = prompt if prompt is not None else "Please enter your message here"
    print("\n" + prompt_str + "\n")

    while True:
        # Prompt the user for a new line to add to the message
        result = input_str(
            "Enter a new line to add to the message (Enter 'DONE' to finish): ",
            lower_case=False,
        )
        if result.is_err():
            return result.propagate()
        newline: str = result.unwrap()
        if newline.upper() == "DONE":
            print(f"Message = \n\n{message}\n")
            option_result = input_option(
                confirm_menu, prompt="Confirm the entered `Message` text"
            )
            if option_result.is_err():
                return Result[str].err(option_result.unwrap_err())
            idx, _ = option_result.unwrap()
            match idx:
                case 1:  # Continue Adding Lines
                    continue
                case 2:  # Clear Message and Restart
                    message = ""
                    continue
                case _:  # Exit the loop if the user is done entering lines
                    break

        # Append the new line to the message, followed by a newline character
        message += f"{newline}\n"

    return Result.ok(message)
