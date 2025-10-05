from pylms.cli.option_input import input_option
from pylms.cli.path_input import input_path
from pylms.cli.select_student import select_student
from pylms.constants import NAME
from pylms.errors import Result
from pylms.utils.data.data_read import read_data
from pylms.utils.data.datastore import DataStore
import pandas as pd


def provide_serials(ds: DataStore) -> Result[list[int]]:
    provide_serials_formats: list[str] = [
        "Provide student serials as .txt file (one serial no per line)",
        "Provide student serials as .csv file (one serial no per line)",
        "Provide student serials as .xlsx file (single col with serial nums)",
        "Provide student serials as input delimited by either ';' or ','",
    ]

    # Prompt user to select the format of the email input
    result = input_option(
        provide_serials_formats, prompt="Select the format to provide the serials in"
    )
    if result.is_err():
        return Result[list[int]].err(result.unwrap_err())
    pos, format_msg = result.unwrap()
    input_serials: list[int] = []
    match pos:
        case 1 | 2:
            # Get the file path or input string based on the selected format
            path_result = input_path(f"{format_msg}: ")
            if path_result.is_err():
                return Result[list[int]].err(path_result.unwrap_err())
            filepath = path_result.unwrap()
            # Read serials from a text or CSV file, one serial per line
            if not filepath.suffix.endswith("txt") and not filepath.suffix.endswith(
                "csv"
            ):
                return Result[list[int]].err(
                    ValueError(
                        f"The file provided is not a .txt or .csv file: {filepath}"
                    )
                )
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    serials_str: list[str] = [
                        line.strip() for line in file if line.strip() != ""
                    ]
                    serials: list[int] = [int(s) for s in serials_str]
                    input_serials.extend(serials)
            except FileNotFoundError as e:
                return Result[list[int]].err(
                    FileNotFoundError(
                        f"The file was not found: {filepath}, with error: {e}"
                    )
                )
            except ValueError:
                return Result[list[int]].err(
                    ValueError(
                        "One or more serial numbers in the file could not be converted to integers."
                    )
                )
        case 3:
            # Get the file path or input string based on the selected format
            path_result = input_path(f"{format_msg}: ")
            if path_result.is_err():
                return Result[list[int]].err(path_result.unwrap_err())
            filepath = path_result.unwrap()
            # Read serials from an Excel file with a single column
            if not filepath.suffix.endswith("xlsx"):
                return Result[list[int]].err(
                    ValueError(f"The file provided is not a .xlsx file: {filepath}")
                )
            try:
                data: pd.DataFrame = read_data(filepath)
                if data.empty or len(data.columns.tolist()) != 1:
                    return Result[list[int]].err(
                        ValueError(
                            "The Excel file must contain exactly one column with serial numbers."
                        )
                    )
                serials = [int(s) for s in data.iloc[:, 0].tolist()]
                input_serials.extend(serials)
            except FileNotFoundError as e:
                return Result[list[int]].err(
                    FileNotFoundError(
                        f"The file was not found: {filepath}, with error: {e}"
                    )
                )
            except ValueError:
                return Result[list[int]].err(
                    ValueError(
                        "One or more serial numbers in the Excel file could not be converted to integers."
                    )
                )
        case _:
            input_serials.extend(select_student(ds))

    valid_serials: list[int] = [
        s for s in input_serials if 1 <= s <= ds.as_ref().shape[0]
    ]
    valid_serials = list(set(valid_serials))  # remove duplicates
    valid_serials.sort()  # sort the list

    names: pd.Series = ds.pretty().loc[:, NAME]
    for serial in valid_serials:
        print(f"You have selected Student {serial}: {names[serial - 1]}")
    print()

    option_result = input_option(
        ["Yes, proceed", "No, cancel"], prompt="Proceed with these serials?"
    )
    if option_result.is_err():
        return Result[list[int]].err(option_result.unwrap_err())
    idx, _ = option_result.unwrap()

    if idx != 1:
        return Result[list[int]].err(ValueError("Operation cancelled by user."))
    return Result[list[int]].ok(valid_serials)
