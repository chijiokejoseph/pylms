from pathlib import Path
from typing import Callable, Literal, Self, final, override

import pandas as pd

from ..constants import (
    COMMA,
    DATA_COLUMNS,
    NAME,
    PHONE,
    SEMI,
)
from ..errors import LMSError, Result, Unit, eprint
from .data_read import read
from .datastream import DataStream

type Validator = Callable[[pd.DataFrame], bool]


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
    return lambda x: x.replace(delim, "")


def validate(test_data: pd.DataFrame) -> bool:
    """Validate that `test_data` contains the expected columns in order.

    The validation enforces that `test_data` has at least the columns listed in
    the module constant `DATA_COLUMNS` and that the first N columns match the
    expected names and order.

    Args:
        test_data (pd.DataFrame): DataFrame to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    # Convert column Index to a plain list for easier comparison operations.
    data_columns: list[str] = test_data.columns.tolist()
    # compare lengths of expected and actual columns
    if len(data_columns) > len(DATA_COLUMNS):
        # Too many columns might indicate the user is attempting to reinitialize
        # an already-initialized DataStore or provided an unexpected file layout.
        eprint(
            f"data argument has more columns than the expected number of columns required for the first initialization of the DataStore. These required columns are {DATA_COLUMNS}. \nCheck it is possible that you are trying to reinitialize a DataStore that has already been initialized."
        )
        return False
    elif len(data_columns) < len(DATA_COLUMNS):
        # Not enough columns — cannot initialize.
        eprint(
            f"data argument has less columns than the expected number of columns required for the first initialization of the DataStore. These required columns are {DATA_COLUMNS}. \nCheck it is possible that you are trying to reinitialize a DataStore that has already been initialized."
        )
        return False
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
        eprint("Data contains mismatched cols")
        for col in mismatched_cols:
            eprint(col)
        return False
    return True


@final
class DataStore(DataStream[pd.DataFrame]):
    """A DataStream specialized for pandas DataFrames with a required schema.

    `DataStore` enforces the presence and order of columns defined in
    `DATA_COLUMNS` and provides helper methods for common transformations and
    persistence (export to Excel, pretty-print transformations, etc.).
    """

    @classmethod
    def from_local(cls, path: Path) -> Result[Self]:
        """Create a DataStore by reading from a local file.

        This convenience constructor reads an Excel or CSV file from `path`,
        preserving NA handling for initialization, and returns a validated
        `DataStore` wrapped in a `Result`.

        Args:
            path (Path): Path to the source Excel or CSV file.

        Returns:
            Result[DataStore]: Ok(DataStore) on success; Err on failure.
        """
        # Use the shared file-read helper which returns a Result to gracefully
        # handle common I/O and parse errors.
        data = read(path, keep_na=True)
        if data.is_err():
            # Propagate the error Result so callers receive context.
            return data.propagate()
        data = data.unwrap()
        # Delegate to from_data for validation and construction.
        return cls.from_data(data)

    @classmethod
    def from_data(cls, data: pd.DataFrame) -> Result[Self]:
        """Construct a DataStore from an existing DataFrame.

        The function will attempt to select the columns in `DATA_COLUMNS` from
        `data`, validate the selection, and construct a `DataStore`. If required
        columns are missing or validation fails an error `Result` will be
        returned.

        Args:
            data (pd.DataFrame): Source DataFrame containing at least the
                columns defined in `DATA_COLUMNS`.

        Returns:
            Result[DataStore]: Ok(DataStore) on success; Err on failure.
        """
        try:
            # Attempt to slice the DataFrame to only the expected columns.
            subset_data: pd.DataFrame = data[DATA_COLUMNS]
        except KeyError as e:
            # Missing columns — produce a helpful message for debugging.
            msg = f"Failed at from_local, failed to validate the passed in as argument to `data`, because it lacked required columns stored in the constant `DATA_COLUMNS.\nError encountered: {e}`"
            eprint(msg)
            return Result.err(e)

        # Validate the sliced DataFrame for ordering/names.
        if not validate(subset_data):
            msg = "Failed at from_local, failed to validate data stored at the file path specified as argument to `path`"
            eprint(msg)
            return Result.err(LMSError(msg))

        # Create the DataStore using the validated subset, then attach the
        # full original DataFrame (including any extra columns) to the instance.
        ds: Self = cls(subset_data)
        ds.data = data
        return Result.ok(ds)

    def __init__(
        self, data: pd.DataFrame | DataStream[pd.DataFrame], prefilled: bool = False
    ) -> None:
        """Initialize a DataStore instance.

        Args:
            data (pd.DataFrame | DataStream[pd.DataFrame]): Source data or
                DataStream providing the data.
            prefilled (bool): Whether the store contains dummy/prefilled data.
                Defaults to False.

        The initializer will extract the underlying DataFrame (if a
        `DataStream` is provided) and validate the data against the expected
        schema (`validate`) before storing it.
        """
        # If a DataStream was passed, call it to get the actual DataFrame value.
        # Copying here ensures we don't accidentally share mutable state between
        # the caller and this instance when a DataStream was provided.
        true_data: pd.DataFrame = (
            data.as_clone() if isinstance(data, DataStream) else data.copy()
        )
        # Record whether this store contains prefilling/demo data.
        self.prefilled: bool = prefilled
        # Delegate to the DataStream initializer with the module-level `validate`
        # function enforcing the required schema at construction time.
        super().__init__(true_data, validate)

    def copy_from(self, ds: Self) -> None:
        # Copy both the stored data and the `prefilled` marker from another store.
        # The assignment to `data` uses the setter which validates the schema.
        self.data = ds.data
        self.prefilled = ds.prefilled

    def pretty(self) -> pd.DataFrame:
        data: pd.DataFrame = self.as_clone()

        # Remove formatting markers from display fields to make the output
        # friendlier for users (commas/semi-colons used as internal markers).
        data[NAME] = data[NAME].astype(str).apply(apply_fn(COMMA))  # pyright: ignore [reportUnknownMemberType]
        data[PHONE] = data[PHONE].astype(str).apply(apply_fn(SEMI))  # pyright: ignore [reportUnknownMemberType]
        return data

    def to_pretty(self) -> pd.DataFrame:
        # Produce a reduced view containing only display fields; operate on a copy
        # to avoid mutating the store's internal value.
        data = self.as_ref()
        data = data[[NAME, PHONE]].copy()
        data[NAME] = data[NAME].astype(str).apply(apply_fn(COMMA))  # pyright: ignore [reportUnknownMemberType]
        data[PHONE] = data[PHONE].astype(str).apply(apply_fn(SEMI))  # pyright: ignore [reportUnknownMemberType]
        return data

    @override
    def to_excel(
        self, path: Path, style: Literal["pretty", "normal"] = "normal"
    ) -> Result[Unit]:
        """Persist the stored data to an Excel file.

        Args:
            path (Path): Destination path for the Excel file.
            style (Literal['pretty', 'normal']): If 'pretty' the stored data is
                converted via `pretty()` before writing. Defaults to 'normal'.

        Raises:
            OSError: Propagates filesystem/pandas I/O errors.
        """
        # Choose whether to transform the data for presentation prior to writing.
        if style == "pretty":
            data: pd.DataFrame = self.pretty()
        else:
            # as_ref returns the stored object by reference; pandas will read from it.
            data = self.as_ref()

        try:
            data.to_excel(path, index=False)  # pyright: ignore [reportUnknownMemberType]
        except Exception as e:
            msg = str(e)
            eprint(msg)
            return Result.err(msg)

        return Result.unit()

    @property
    def data(self) -> pd.DataFrame:
        """Return a cloned copy of the underlying DataFrame.

        Returns:
            pd.DataFrame: A copy of the stored data.
        """
        # Return a clone to protect internal state from accidental mutation by callers.
        return self.as_clone()

    @data.setter
    def data(self, data: pd.DataFrame) -> None:
        """Validate and set the underlying DataFrame value.

        The setter performs a column-name and ordering validation against
        `DATA_COLUMNS`. If validation fails a `DataStream` instance will raise
        an exception and the setter will not modify the stored value.

        Args:
            data (pd.DataFrame): New DataFrame to set as the store's value.
        """

        # Define a lightweight validator used to check whether the incoming
        # DataFrame matches the required schema for the store.
        def validator(test_data: pd.DataFrame) -> bool:
            input_cols: list[str] = test_data.columns.tolist()
            expected_cols: list[str] = DATA_COLUMNS
            if len(input_cols) < len(expected_cols):
                # Not enough columns to satisfy the expected schema.
                return False

            # Compare only the first N columns (where N == len(expected_cols))
            # so extra trailing columns are tolerated when present in the source.
            input_subset: list[str] = input_cols[: len(expected_cols)]
            for expected, actual in zip(expected_cols, input_subset):
                if expected != actual:
                    return False
            return True

        # Validate by constructing a temporary DataStream; it will raise if invalid.
        _ = DataStream(data, validator)
        # Store the full DataFrame (including any additional columns) in the
        # internal single-element tuple. This mirrors previous behavior where
        # both the required columns and any extras are preserved.
        self._value = (data,)
