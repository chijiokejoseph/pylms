import re
from pathlib import Path
from typing import Self, final, override

import polars as pl

from ..constants import COMMA, COMMA_DELIM, DATA_COLUMNS, NAME, PHONE, SEMI
from ..errors import Result, Unit, eprint
from .datastream import DataStream
from .utils import validate, write


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
