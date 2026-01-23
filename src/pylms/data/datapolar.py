from collections.abc import Callable
from pathlib import Path
import re
from typing import Self, final, override

import polars as pl

from pylms.constants import COMMA, COMMA_DELIM, DATA_COLUMNS, NAME, PHONE, SEMI
from pylms.errors import Result, Unit, eprint

type Stream = DataStream


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


class DataStream:
    """Wrapper for Polars DataFrame with validation and I/O operations."""
    _value: tuple[pl.DataFrame]

    def __init__(self, data: pl.DataFrame | Stream) -> None:
        """Initialize DataStream with DataFrame or another DataStream.
        
        Args:
            data (pl.DataFrame | Stream): Source data.
        """
        # Extract DataFrame reference if input is DataStream
        data = data.as_ref() if isinstance(data, DataStream) else data
        self._value = (data,)

    @classmethod
    def new(
        cls,
        data: pl.DataFrame | Stream,
        validator: Callable[[pl.DataFrame], tuple[bool, str]] | None = None,
    ) -> Result[Self]:
        """Create new DataStream with optional validation.
        
        Args:
            data (pl.DataFrame | Stream): Source data.
            validator (Callable | None): Optional validation function.
            
        Returns:
            Result[Self]: Success with DataStream or error message.
        """
        # Clone data to avoid mutations
        value = data.as_clone() if isinstance(data, DataStream) else data.clone()

        if validator is None:
            return Result.ok(cls(value))
        test, msg = validator(value)
        if test:
            return Result.ok(cls(value))

        return Result.err(msg)

    def as_ref(self) -> pl.DataFrame:
        """Get reference to underlying DataFrame.
        
        Returns:
            pl.DataFrame: Reference to stored DataFrame.
        """
        return self._value[0]

    def as_clone(self) -> pl.DataFrame:
        """Get clone of underlying DataFrame.
        
        Returns:
            pl.DataFrame: Clone of stored DataFrame.
        """
        return self.as_ref().clone()

    def write(self, path: Path, *, worksheet: str | None = None) -> Result[Unit]:
        """Write DataFrame to file.
        
        Args:
            path (Path): Output file path.
            worksheet (str | None): Excel worksheet name.
            
        Returns:
            Result[Unit]: Success or error message.
        """
        data = self.as_ref()
        return write(data, path, worksheet=worksheet)

    @classmethod
    def verify(
        cls, data: pl.DataFrame, validator: Callable[[pl.DataFrame], tuple[bool, str]]
    ) -> Result[Unit]:
        """Verify DataFrame against validator without creating instance.
        
        Args:
            data (pl.DataFrame): DataFrame to validate.
            validator (Callable): Validation function.
            
        Returns:
            Result[Unit]: Success or error message.
        """
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


@final
class DataStore(DataStream):
    """DataStream with strict validation for student data storage."""
    
    def __init__(self, value: pl.DataFrame | DataStream) -> None:
        """Initialize DataStore with prefilled flag.
        
        Args:
            value (pl.DataFrame | DataStream): Source data.
        """
        self._prefilled: bool = True
        super().__init__(value)

    @property
    def prefilled(self) -> bool:
        return self._prefilled

    @classmethod
    def init(
        cls,
        data: pl.DataFrame | DataStream,
    ) -> Result[Self]:
        """Initialize DataStore with column validation.
        
        Args:
            data (pl.DataFrame | DataStream): Source data with required columns.
            
        Returns:
            Result[Self]: Success with DataStore or validation error.
        """
        value = DataStream.new(data, validate)
        if value.is_err():
            return value.propagate()

        value = value.unwrap()
        value = cls(value)
        value._prefilled = False
        return Result.ok(value)

    @classmethod
    def from_data(cls, data: pl.DataFrame) -> Result[Self]:
        """Create a DataStore from existing DataFrame with attendance data.
        
        This method validates that the input DataFrame contains all required columns
        and that any additional columns follow the date format (DD/MM/YYYY) for
        attendance tracking. Unlike init(), this method preserves the full DataFrame
        including date columns for attendance data.
        
        Args:
            data (pl.DataFrame): DataFrame containing student data with required
                columns and optional date columns for attendance tracking.
                
        Returns:
            Result[Self]: Success with DataStore instance, or error with validation
                message if required columns are missing or invalid columns exist.
                
        Note:
            The method expects date columns to follow DD/MM/YYYY format and will
            reject any non-date columns beyond the required DATA_COLUMNS.
        """
        # Check if all required columns are present
        data_columns = set(data.columns)
        required = set(DATA_COLUMNS)

        if not required.issubset(data_columns):
            missing_cols = list(required.difference(data_columns))
            col_print = COMMA_DELIM.join(missing_cols)
            msg = f"data is missing the following columns: '{col_print}'"
            eprint(msg)
            return Result.err(msg)

        # Extract required columns for validation
        subset = data[DATA_COLUMNS]
        
        # Validate additional columns are date-formatted (MM/DD/YYYY)
        date_cols = [col for col in data.columns if col not in DATA_COLUMNS]
        reg = re.compile(r"^\d{2}/\d{2}/\d{4}$")
        not_date_cols = [col for col in date_cols if reg.fullmatch(col) is None]

        if len(not_date_cols) > 0:
            msg = f"data contains the following non-date columns: {not_date_cols}"
            eprint(msg)
            return Result.err(msg)
        
        # Initialize DataStore with required columns only for validation
        ds = cls.init(subset)
        if ds.is_err():
            return ds.propagate()

        # Replace with full DataFrame including date columns
        ds = ds.unwrap()
        ds._value = (data,)  # Store complete DataFrame with attendance data
        ds._prefilled = False
        return Result.ok(ds)

    def pretty(self) -> pl.DataFrame:
        """Return cleaned DataFrame with formatting removed.
        
        Returns:
            pl.DataFrame: DataFrame with commas and semicolons removed.
        """
        return (
            self.as_ref()
            .lazy()
            .with_columns(
                pl.col(NAME).str.replace(COMMA, "").alias(NAME),
                pl.col(PHONE).str.replace(SEMI, ""),
            )
            .collect()
        )

    def copy_from(self, data: pl.DataFrame | DataStream) -> Result[Unit]:
        """Replace current data with validated input data.
        
        Args:
            data (pl.DataFrame | DataStream): New data to copy.
            
        Returns:
            Result[Unit]: Success or validation error.
        """
        # Extract DataFrame and validate
        data_in = data.as_ref() if isinstance(data, DataStream) else data  
        valid = self.from_data(data_in)
        if valid.is_err():
            return valid.propagate()

        # Replace current data
        valid = valid.unwrap().as_ref()
        self._value = (valid,)
        self._prefilled = False
        return Result.unit()

    @override
    def write(
        self, path: Path, *, worksheet: str | None = None, pretty: bool | None = None
    ) -> Result[Unit]:
        """Write DataStore to file with optional formatting.
        
        Args:
            path (Path): Output file path.
            worksheet (str | None): Excel worksheet name.
            pretty (bool | None): Whether to apply formatting cleanup.
            
        Returns:
            Result[Unit]: Success or error message.
        """
        # Choose formatted or raw data
        if pretty is not None and pretty:
            data = self.pretty()
        else:
            data = self.as_ref()

        return write(data, path, worksheet=worksheet)
