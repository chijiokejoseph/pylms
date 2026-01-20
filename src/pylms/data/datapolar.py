from collections.abc import Callable
from pathlib import Path
from typing import Self, override

import polars as pl

from pylms.constants import COMMA, COMMA_DELIM, NAME, PHONE, SEMI, DATA_COLUMNS
from pylms.errors import Result, Unit, eprint

type Stream = DataStream


def write(
    data: pl.DataFrame, path: Path, *, worksheet: str | None = None
) -> Result[Unit]:
    parent = path.parent
    if not parent.exists():
        msg = f"Parent path specified: '{parent} does not exist"
        eprint(msg)
        return Result.err(msg)

    try:
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


class DataStream:
    _value: tuple[pl.DataFrame]

    def __init__(self, data: pl.DataFrame | Stream) -> None:
        data = data.as_ref() if isinstance(data, DataStream) else data
        self._value = (data,)

    @classmethod
    def new(
        cls,
        data: pl.DataFrame | Stream,
        validator: Callable[[pl.DataFrame], tuple[bool, str]] | None = None,
    ) -> Result[Self]:
        value = data.as_clone() if isinstance(data, DataStream) else data.clone()

        if validator is None:
            return Result.ok(cls(value))
        test, msg = validator(value)
        if test:
            return Result.ok(cls(value))

        return Result.err(msg)

    def as_ref(self) -> pl.DataFrame:
        return self._value[0]

    def as_clone(self) -> pl.DataFrame:
        return self.as_ref().clone()

    def write(self, path: Path, *, worksheet: str | None = None) -> Result[Unit]:
        data = self.as_ref()
        return write(data, path, worksheet=worksheet)

    @classmethod
    def verify(
        cls, data: pl.DataFrame, validator: Callable[[pl.DataFrame], tuple[bool, str]]
    ) -> Result[Unit]:
        result = DataStream.new(data, validator)
        result.print_if_err()
        if result.is_err():
            return result.propagate()

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
    data_columns: list[str] = test_data.columns
    # compare lengths of expected and actual columns
    if len(data_columns) > len(DATA_COLUMNS):
        # Too many columns might indicate the user is attempting to reinitialize
        # an already-initialized DataStore or provided an unexpected file layout.
        msg = (
            f"data argument has more columns than the expected number of columns required for the first initialization of the DataStore. These required columns are {DATA_COLUMNS}. \nCheck it is possible that you are trying to reinitialize a DataStore that has already been initialized."
        )
        return False, msg
    elif len(data_columns) < len(DATA_COLUMNS):
        # Not enough columns — cannot initialize.
        msg = (
            f"data argument has less columns than the expected number of columns required for the first initialization of the DataStore. These required columns are {DATA_COLUMNS}. \nCheck it is possible that you are trying to reinitialize a DataStore that has already been initialized."
        )
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
        msg = (f"Data contains mismatched cols\n{cols_print}")
        return False, msg
    return True, ""

class DataStore(DataStream):
    def __init__(self, value: pl.DataFrame | DataStream) -> None:
        self._prefilled: bool = True
        super().__init__(value)

    @classmethod
    def init(
        cls,
        data: pl.DataFrame | DataStream,
    ) -> Result[Self]:
        value = DataStream.new(data, validate)
        if value.is_err():
            return value.propagate()

        value = value.unwrap()
        value = cls(value)
        value._prefilled = False
        return Result.ok(value)

    @classmethod
    def from_data(cls, data: pl.DataFrame) -> Result[Self]:
        missing_cols = [col for col in DATA_COLUMNS if col not in data.columns]
        if len(missing_cols) > 0:
            cols = COMMA_DELIM.join(missing_cols)
            msg = f"Columns: '{cols}' are required but missing"
            return Result.err(msg)
        
        subset = data[DATA_COLUMNS]
        ds = cls.init(subset)
        if ds.is_err():
            return ds.propagate()

        ds = ds.unwrap()
        ds._value = (data,)
        return Result.ok(ds)


    def pretty(self) -> pl.DataFrame:
        return (
            self.as_ref()
            .lazy()
            .with_columns(
                pl.col(NAME).str.replace(COMMA, "").alias(NAME),
                pl.col(PHONE).str.replace(SEMI, ""),
            )
            .collect()
        )

    @override
    def write(
        self, path: Path, *, worksheet: str | None = None, pretty: bool | None = None
    ) -> Result[Unit]:
        if pretty is not None and pretty:
            data = self.pretty()
        else:
            data = self.as_ref()

        return write(data, path, worksheet=worksheet)
