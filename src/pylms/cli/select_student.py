from math import floor, log10
from typing import NamedTuple

import pandas as pd

from ..cli_utils import parse_class_nums
from ..constants import NAME
from ..data import DataStore
from ..errors import Result
from .input_with_quit import input_fn


class PrintSize(NamedTuple):
    """Named tuple holding maximum sizes for printing student numbers and names.

    Attributes:
        max_num_size (int): Maximum width for student number display.
        max_name_size (int): Maximum width for student name display.
    """

    max_num_size: int
    max_name_size: int


def det_max_printout_sizes(possible_names: list[str]) -> PrintSize:
    """Determine maximum print widths for numbers and names.

    Calculates the width required to display student serial numbers and names
    based on the provided list of names.

    Args:
        possible_names (list[str]): List of student names.

    Returns:
        PrintSize: Named tuple containing `max_num_size` and `max_name_size`.
    """
    # Initialize minimum width for student number display
    max_num_size: int = 2

    # Calculate the logarithm base 10 of the number of names to determine digit width
    log_value: float = log10(len(possible_names))

    # Floor the log value to get integer part
    floor_log_value: float = floor(log_value)

    # Allocate space for the number display
    allocated_space: int = int(floor_log_value) + 1
    max_num_size += allocated_space

    # Initialize minimum width for student name display
    max_name_size: int = 8

    # Add the length of the longest name to the width
    max_name_size += max([len(each_name) for each_name in possible_names])
    return PrintSize(max_num_size, max_name_size)


def add_name_printout(num: int, name: str, size: PrintSize) -> str:
    """Format a single student's serial number and name into a printable string.

    Args:
        num (int): Student's serial number (1-based).
        name (str): Student's name.
        size (PrintSize): Formatting widths (max_num_size, max_name_size).

    Returns:
        str: Formatted string with aligned number and name.
    """
    # Format the student number with a closing parenthesis
    num_format: str = f"{num}.)"
    max_num_size, max_name_size = size

    # Return the formatted string with aligned number and name
    return f"{num_format:<{max_num_size}}\t{name:<{max_name_size}}"


def add_names_printout(all_names: list[str], names_serials: list[int]) -> str:
    """Format multiple students into a multi-column printable string.

    Args:
        all_names (list[str]): List of all student names.
        names_serials (list[int]): List of 1-based student serial numbers to include.

    Returns:
        str: Multi-line formatted string for the selected students.
    """
    # Determine the print size based on all names
    size: PrintSize = det_max_printout_sizes(all_names)

    # Convert serial numbers to zero-based indices
    names_indices: list[int] = [serial - 1 for serial in names_serials]

    # Get the names corresponding to the indices
    names_list = [all_names[i] for i in names_indices]

    # Initialize the line string
    line: str = ""

    # Append formatted name printouts for each student
    for idx, name in zip(names_serials, names_list):
        line += add_name_printout(idx, name, size)
    return line.strip() + "\n"


def printout_names(names_list: list[str]) -> None:
    """Print a formatted multi-column list of student names.

    Args:
        names_list (list[str]): List of student names to print.

    Returns:
        None
    """
    # Get the total number of names
    names_len: int = len(names_list)

    # Number of names to print per line
    num_names_per_line: int = 3

    # Initialize the string to hold the formatted names
    names_print: str = ""

    # Iterate over the names in chunks of num_names_per_line
    for serial in range(1, names_len + 1, num_names_per_line):
        diff: int = names_len - serial
        if diff > num_names_per_line:
            # Create indices for a full line of names
            indices: list[int] = [
                serial + increment for increment in range(num_names_per_line)
            ]
        else:
            # Create indices for the remaining names
            indices = [serial + increment for increment in range(diff)]

        # Append the formatted names for the current line
        names_print += add_names_printout(names_list, indices)

    # Print all formatted names
    print(names_print)


def select_student(ds: DataStore) -> Result[list[int]]:
    """Prompt user to select students by serial numbers and return selection.

    Presents instructions and a formatted list of student names, prompts the
    user to enter serial numbers (single, comma-separated, or ranges), parses
    the input and returns the selected serial numbers.

    Args:
        ds (DataStore): The data store containing student information.

    Returns:
        Result[list[int]]: Ok containing a list of selected 1-based serial numbers,
            or an Err propagated from input/validation helpers.
    """
    # Get a pretty formatted DataFrame of the data store
    pretty_data: pd.DataFrame = ds.pretty()

    # Extract the list of student names
    names: list[str] = pretty_data[NAME].astype(str).tolist()

    # Instruction message for the user
    instruction: str = """
You can enter the students serial number using one of the following formats:
    i. Enter comma separated values of the target students' serial numbers.
    e.g., "Enter Student(s) S/N: 1, 2, 3"
    ii. Enter a range of target students' serials
    e.g., "Enter Student(s) S/N: 1 - 5
    """
    # Print the instruction message
    print(instruction)

    # Print the list of student names formatted
    printout_names(names)

    # Prompt the user to enter student serial numbers
    result = input_fn("Enter Student (S/N): ")
    if result.is_err():
        return result.propagate()
    selection = result.unwrap()

    # Parse the input string into a list of serial numbers
    student_serials = parse_class_nums(selection)
    if student_serials.is_err():
        return student_serials.propagate()

    student_serials = student_serials.unwrap()
    # Sort the serial numbers
    student_serials.sort()

    # Return the list of selected student serial numbers
    return Result.ok(student_serials)
