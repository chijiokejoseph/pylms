from typing import Callable, cast

from pylms.cli.custom_inputs import input_num
from pylms.record import RecordStatus
from pylms.utils.date import retrieve_dates


def input_record(target_date: str, options: list[RecordStatus]) -> RecordStatus:
    class_dates: list[str] = retrieve_dates()
    print("\nSelect from the following: ")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    class_num: int = class_dates.index(target_date) + 1
    prompt: str = f"""
From the options presented above listed {1} - {len(options)},
Please Select which of the following Record Status should be set for the entire class 
\nFor Class {class_num} held on {target_date} (only integers from 1 - {len(options)} are allowed):  """

    def validate_input(entered_num: int) -> bool:
        return 1 <= entered_num <= len(options)

    validate_fn = cast(Callable[[float | int], bool], validate_input)

    selection_temp: float | int = input_num(prompt, "int", test_fn=validate_fn)
    selection: int = cast(int, selection_temp)
    selected_record: RecordStatus = options[selection - 1]
    print(f"You have selected: {selected_record}")
    return selected_record
