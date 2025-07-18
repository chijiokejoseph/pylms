from math import floor, log10
from typing import NamedTuple

import pandas as pd

from pylms.cli.input_with_quit import input_fn
from pylms.cli.utils import parse_to_serials
from pylms.constants import NAME
from pylms.utils import DataStore


class PrintSize(NamedTuple):
    max_num_size: int
    max_name_size: int


def det_max_printout_sizes(possible_names: list[str]) -> PrintSize:
    max_num_size: int = 2
    log_value: float = log10(len(possible_names))
    floor_log_value: float = floor(log_value)
    allocated_space: int = int(floor_log_value) + 1
    max_num_size += allocated_space

    max_name_size: int = 8
    max_name_size += max([len(each_name) for each_name in possible_names])
    return PrintSize(max_num_size, max_name_size)


def add_name_printout(num: int, name: str, size: PrintSize) -> str:
    num_format: str = f"{num}.)"
    max_num_size, max_name_size = size
    return f"{num_format:<{max_num_size}}\t{name:<{max_name_size}}"


def add_names_printout(all_names: list[str], names_serials: list[int]) -> str:
    # get print size from the the list of possible names `all_names`
    size: PrintSize = det_max_printout_sizes(all_names)

    # get indices from serials entered
    names_indices: list[int] = [serial - 1 for serial in names_serials]

    # extract the list of names by indexing all_names with each index of `names_indices`
    names_list = [all_names[i] for i in names_indices]

    line: str = ""
    for idx, name in zip(names_serials, names_list):
        line += add_name_printout(idx, name, size)
    return line.strip() + "\n"


def printout_names(names_list: list[str]) -> None:
    names_len: int = len(names_list)
    num_names_per_line: int = 3
    names_print: str = ""
    for serial in range(1, names_len + 1, num_names_per_line):
        diff: int = names_len - serial
        if diff > num_names_per_line:
            indices: list[int] = [
                serial + increment for increment in range(num_names_per_line)
            ]
        else:
            indices = [serial + increment for increment in range(diff)]
        names_print += add_names_printout(names_list, indices)
    print(names_print)


def select_student(ds: DataStore) -> list[int]:
    pretty_data: pd.DataFrame = ds.pretty()
    names: list[str] = pretty_data[NAME].tolist()
    instruction: str = """
You can enter the students serial number using one of the following formats:
    i. Enter comma separated values of the target students' serial numbers.
    e.g., "Enter Student(s) S/N: 1, 2, 3"
    ii. Enter a range of target students' serials 
    e.g., "Enter Student(s) S/N: 1 - 5
    """
    print(instruction)
    printout_names(names)
    selection: str = input_fn("Enter Student(s) S/N: ")
    student_serials: list[int] = parse_to_serials(selection)
    student_serials.sort()
    for serial in student_serials:
        print(f"You have selected Student {serial}: {names[serial-1]}")
    print()
    return student_serials
