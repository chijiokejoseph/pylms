from pathlib import Path

import polars.selectors as cs

from ..data import DataStore, read
from ..errors import Result, eprint
from ..info import print_info, printpass
from .print_selection import print_selection
from .select_serials import select_serials


def select_path(ds: DataStore, path: Path) -> Result[list[tuple[int, str]]]:
    serials: list[int] = []

    # Process based on file extension
    if path.suffix in [".txt", ".csv"]:
        # Read text/csv file line by line
        try:
            with open(path, "r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip() != ""]
                serials = [int(s) for s in lines]
        except FileNotFoundError:
            msg = f"File not found: {path}"
            eprint(msg)
            return Result.err(msg)
        except ValueError:
            msg = "File contains non-numeric values"
            eprint(msg)
            return Result.err(msg)

    elif path.suffix == ".xlsx":
        # Read Excel file and get first numeric column
        data_result = read(path)
        if data_result.is_err():
            return data_result.propagate()

        data = data_result.unwrap()

        data = data.with_columns(cs.numeric())

        if data.height == 0:
            msg = "No numeric columns found in Excel file"
            eprint(msg)
            return Result.err(msg)

        # Get serials from first numeric column
        serials = data.to_series().to_list()

    else:
        msg = f"Unsupported file type: {path.suffix}. Use .txt, .csv, or .xlsx"
        return Result.err(msg)

    # Validate serials using select_serials
    if len(serials) == 0:
        msg = "No serial numbers found in file"
        return Result.err(msg)

    # Use select_serials to validate and get student info
    filter_result = select_serials(ds, serials)
    if filter_result.is_err():
        return filter_result.propagate()

    # Display selection
    selections = filter_result.unwrap()
    print_info(f"Found {len(selections)} student(s) from file")
    print_selection(selections)

    printpass(f"Selected {len(selections)} student(s) from file")
    return Result.ok(selections)
