from ..info import print_info


def run_prompt(menu: list[str]) -> str:
    """
    main prompt function that interacts with the user. It prints out a series of options gotten from the argument passed to the `menu` parameter of the function. For each string in the list `menu` an option num which counts from 1 is printed alongside the option itself. The function returns the response entered by the user.

    :param menu: (list[str]): A list of options that make up the main menu of the program.
    :type menu: List[str]

    :return: (str): The response entered by the user. The response is trimmed of whitespaces and lowercased before being returned.
    :rtype: Str
    """
    intro: str = "Hello I'm the LMS Bot Jayce 🎓. \nI have printed out below a list of menu options select one and I'll provide assistance right away\n"
    print_info(intro)

    for i, option in enumerate(menu, start=1):
        print(f"{i}. {option}")
    print()

    response: str = input("Select an option: ").lower().strip()
    return response
