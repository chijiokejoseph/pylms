from ..info import print_info


def run_prompt(menu: list[str]) -> str:
    """Display a menu prompt and return the user's response.

    Prints an introductory message, enumerates the provided `menu` options
    (numbered starting at 1), and prompts the user to select an option.
    The returned string is lower-cased and trimmed of surrounding whitespace.

    Args:
        menu (list[str]): The list of option strings to present to the user.

    Returns:
        str: The user's response, lower-cased and stripped of surrounding whitespace.
    """
    intro: str = "Hello I'm the LMS Bot Jayce 🎓. \nI have printed out below a list of menu options select one and I'll provide assistance right away\n"
    print_info(intro)

    for i, option in enumerate(menu, start=1):
        print(f"{i}. {option}")
    print()

    response: str = input("Select an option: ").lower().strip()
    return response
