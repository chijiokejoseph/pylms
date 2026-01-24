from ..cli import input_option, input_str
from ..errors import Result


def construct_msg(prompt: str | None = None) -> Result[str]:
    """Construct multi-line message by prompting user for input.
    
    User enters lines one at a time until 'DONE' is entered. Provides options
    to continue adding lines, clear and restart, or proceed with the message.
    
    Args:
        prompt (str | None): Optional custom prompt message.
        
    Returns:
        Result[str]: Success with constructed message or error.
    """
    message: str = ""  # Initialize empty message

    confirm_menu: list[str] = [
        "Continue Adding Lines",
        "Clear Message and Restart",
        "Proceed with Message",
    ]

    prompt_str: str = prompt if prompt is not None else "Please enter your message here"
    print("\n" + prompt_str + "\n")

    while True:
        # Prompt user for new line
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
                case _:  # Proceed with message
                    break

        # Append new line to message
        message += f"{newline}\n"

    return Result.ok(message)
