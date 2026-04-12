from collections.abc import Callable
from pathlib import Path

import polars as pl
import polars.selectors as cs

from ..constants import DATA_COLUMNS
from ..errors import Result, Unit, eprint


def write(
    data: pl.DataFrame, path: Path, *, worksheet: str | None = None
) -> Result[Unit]:
    """Write DataFrame to file in CSV, Excel, or Parquet format.

    Args:
        data (pl.DataFrame): DataFrame to write.
        path (Path): Output file path with extension determining format.
        worksheet (str | None): Excel worksheet name (ignored for other formats).

    Returns:
        Result[Unit]: Success or error with message.
    """
    parent = path.parent
    if not parent.exists():
        msg = f"Parent path specified: '{parent} does not exist"
        eprint(msg)
        return Result.err(msg)

    data = data.with_columns(cs.integer().round(0), cs.float().round(2))

    try:
        # Write based on file extension
        match path.suffix:
            case ".csv":
                data.write_csv(path, include_header=True)
            case ".xlsx":
                _ = data.write_excel(path, worksheet)
            case ".parquet":
                data.write_parquet(path)
            case _:
                msg = f"File output formats are '.csv', '.xlsx' and '.parquet'. Format: '{path.suffix}' not supported"
                eprint(msg)
                return Result.err(msg)

    except Exception as e:
        msg = str(e)
        eprint(msg)
        return Result.err(e)

    return Result.unit()


def apply_fn(delim: str) -> Callable[[str], str]:
    """Return a function that removes a delimiter from strings.

    This helper is used to create small, reusable transformers that strip a
    specific character (for example formatting delimiters) from string values.

    Args:
        delim (str): Character to remove from input strings.

    Returns:
        Callable[[str], str]: Function that accepts a string and returns it with
            all occurrences of `delim` removed.
    """
    # Return a simple closure that calls str.replace; intentionally minimal to
    # keep the transformation cheap when applied over large Series.
    return lambda x: x.replace(delim, "").strip()


def validate(test_data: pl.DataFrame) -> tuple[bool, str]:
    """Validate that `test_data` contains the expected columns in order.

    The validation enforces that `test_data` has at least the columns listed in
    the module constant `DATA_COLUMNS` and that the first N columns match the
    expected names and order.

    Args:
        test_data (pl.DataFrame): DataFrame to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    # Convert column Index to a plain list for easier comparison operations.
    data_columns = test_data.columns
    # compare lengths of expected and actual columns
    if len(data_columns) > len(DATA_COLUMNS):
        # Too many columns might indicate the user is attempting to reinitialize
        # an already-initialized DataStore or provided an unexpected file layout.
        msg = f"data argument has more columns than the expected number of columns required for the first initialization of the DataStore. These required columns are {DATA_COLUMNS}. \nCheck it is possible that you are trying to reinitialize a DataStore that has already been initialized."
        return False, msg

    elif len(data_columns) < len(DATA_COLUMNS):
        # Not enough columns — cannot initialize.
        msg = f"data argument has less columns than the expected number of columns required for the first initialization of the DataStore. These required columns are {DATA_COLUMNS}. \nCheck it is possible that you are trying to reinitialize a DataStore that has already been initialized."
        return False, msg

    else:
        # Length matches expected count; proceed to verify names and order.
        pass

    # comparing that the order and names of expected columns match those of the actual columns.
    mismatched_cols: list[str] = []
    for expected, actual in zip(DATA_COLUMNS, data_columns):
        # Enforce exact match on name and position.
        if expected != actual:
            mismatched_cols.append(f"Expected: '{expected}', got: '{actual}'")

    if len(mismatched_cols) > 0:
        cols_print = "\n".join(mismatched_cols)
        msg = f"Data contains mismatched cols\n{cols_print}"
        return False, msg
    return True, ""
