import pandas as pd

from ..constants import NAME
from ..data import DataStore, read
from ..errors import Result, eprint
from ..info import print_info
from .option_input import input_bool, input_option
from .path_input import input_path
from .students_input import select_student


def provide_serials(ds: DataStore) -> Result[list[int]]:
    """Prompt user to provide serial numbers in a supported format.

    The user is presented with a menu of input formats (plain text, CSV,
    Excel, manual delimited input or interactive selection). The chosen format
    determines how serials are read. After reading and parsing serials the
    function validates each serial to ensure it is within the valid range of
    student rows in `ds`. Duplicates are removed and the list is sorted. The
    user is asked to confirm the selection before the function returns.

    Args:
        ds: The `DataStore` instance used to validate serial ranges and to
            display student names for confirmation.

    Returns:
        Result[list[int]]: Ok(list[int]) on success containing validated serial
            numbers; Err(str) with a descriptive message on failure.

    Raises:
        None: Errors are returned via the `Result` type rather than raised.
    """
    formats: list[str] = [
        "Provide student serials as .txt file (one serial no per line)",
        "Provide student serials as .csv file (one serial no per line)",
        "Provide student serials as .xlsx file (single col with serial nums)",
        "Provide student serials as input delimited by either ';' or ','",
    ]

    # Prompt user to select the format of the email input
    result = input_option(formats, prompt="Select the format to provide the serials in")
    if result.is_err():
        return result.propagate()

    pos, format_msg = result.unwrap()
    input_serials: list[int] = []
    match pos:
        case 1 | 2:
            # Get the file path or input string based on the selected format
            path = input_path(f"{format_msg}: ")
            if path.is_err():
                return path.propagate()
            path = path.unwrap()
            # Read serials from a text or CSV file, one serial per line
            if not path.suffix.endswith("txt") and not path.suffix.endswith("csv"):
                msg = f"The file provided is not a .txt or .csv file: {path}"
                eprint(msg)
                return Result.err(msg)

            try:
                with open(path, "r", encoding="utf-8") as file:
                    serials_str: list[str] = [
                        line.strip() for line in file if line.strip() != ""
                    ]
                    serials: list[int] = [int(s) for s in serials_str]
                    input_serials.extend(serials)
            except FileNotFoundError as e:
                msg = f"The file was not found: {path}, with error: {e}"
                eprint(msg)
                return Result.err(msg)

            except ValueError:
                msg = "One or more serial numbers in the file could not be converted to integers."
                eprint(msg)
                return Result.err(msg)

        case 3:
            # Get the file path or input string based on the selected format
            path = input_path(f"{format_msg}: ")
            if path.is_err():
                return path.propagate()
            path = path.unwrap()
            # Read serials from an Excel file with a single column
            if not path.suffix.endswith("xlsx"):
                msg = f"The file provided is not a .xlsx file: {path}"
                eprint(msg)
                return Result.err(msg)

            try:
                data = read(path)
                if data.is_err():
                    return data.propagate()
                data = data.unwrap()
                if data.empty or len(data.columns.tolist()) != 1:
                    msg = "The Excel file must contain exactly one column with serial numbers."
                    eprint(msg)
                    return Result.err(msg)

                serials = [int(s) for s in data.iloc[:, 0].tolist()]
                input_serials.extend(serials)
            except FileNotFoundError as e:
                msg = f"The file was not found: {path}, with error: {e}"
                eprint(msg)
                return Result.err(msg)

            except ValueError:
                msg = "One or more serial numbers in the Excel file could not be converted to integers."
                eprint(msg)
                return Result.err(msg)

        case _:
            result = select_student(ds)
            if result.is_err():
                return result.propagate()

            result = result.unwrap()
            input_serials.extend(result)

    valid_serials: list[int] = [
        s for s in input_serials if 1 <= s <= ds.as_ref().shape[0]
    ]
    valid_serials = list(set(valid_serials))  # remove duplicates
    valid_serials.sort()  # sort the list

    names: pd.Series = ds.pretty().loc[:, NAME]
    for serial in valid_serials:
        print_info(f"You have selected Student {serial}: {names[serial - 1]}")
    print()

    result = input_bool("Proceed with these serials?")
    if result.is_err():
        return result.propagate()
    choice = result.unwrap()

    if not choice:
        msg = "You have cancelled the operation"
        print_info(msg)
        return Result.err(msg)
    return Result.ok(valid_serials)
