from typing import cast

from pylms.cli.custom_inputs import input_num


def input_option(options: list[str], title: str = "Select from the following: ", prompt: str = "") -> tuple[int, str]:
    print(title)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    print()

    temp = input_num(
        f"{prompt}\nSelect an Option: ",
        "int",
        diagnosis=f"The number you have entered does not match the range 1 - {len(options)}, hence it is invalid",
        test_fn=lambda x: 1 <= x <= len(options),
    )
    choice: int = cast(int, temp)
    choice_idx: int = choice - 1
    return choice, options[choice_idx]
