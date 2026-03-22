import polars as pl

from ..clean import (
    clean_completion_date,
    clean_duplicates,
    clean_email,
    clean_internship,
    clean_na,
    clean_name,
    clean_order,
    clean_phone,
    clean_sort,
    clean_str,
    clean_time,
    clean_training,
)
from ..constants import COHORT, DATA_COLUMNS, DATE, NAME, PHONE
from ..data import DataStore, DataStream
from ..errors import Result


def _clean_new(data_stream: DataStream, ref: DataStore) -> Result[DataStore]:
    """Clean new student data for addition to existing registration data.

    Applies comprehensive data cleaning operations including NA removal,
    string formatting, email/name/phone cleaning, and column reordering.

    Args:
        data_stream (DataStream): Stream containing new student data to clean.

    Returns:
        Result[DataStore]: Success with cleaned DataStore or error.
    """

    def validate_na_removal(test_data: pl.DataFrame) -> tuple[bool, str]:
        contains_na = test_data.null_count().sum_horizontal().item() > 0
        if contains_na:
            return False, "The data has null values"

        return True, ""

    ds_data = ref.as_ref()
    cohort: int = ds_data.item(0, COHORT)
    orientation: str = ds_data.item(0, DATE)

    data = data_stream.as_ref()

    result = clean_na(data, validate_na_removal)
    if result.is_err():
        return result.propagate()

    data = result.unwrap()

    data = clean_str(data, [NAME, PHONE])
    data = clean_email(data)
    data = clean_name(data)

    result = clean_phone(data)
    if result.is_err():
        return result.propagate()

    data = result.unwrap()

    data = data.with_columns(
        [pl.lit(cohort).alias(COHORT), pl.lit(orientation).alias(DATE)]
    )

    data = clean_time(data)
    data = clean_internship(data)
    data = clean_training(data)

    result = clean_completion_date(data)
    if result.is_err():
        return result.propagate()

    data = result.unwrap()

    data = clean_duplicates(data)
    data = clean_sort(data)

    # Get list of columns in data_stream
    columns = data.columns
    # Get columns not in DATA_COLUMNS
    not_data_columns = [col for col in columns if col not in DATA_COLUMNS]
    # Get columns in DATA_COLUMNS
    data_columns = [col for col in columns if col in DATA_COLUMNS]

    # Extract dataframe for only DATA_COLUMNS
    subset1 = data.select(data_columns)
    # Extract dataframe for non-DATA_COLUMNS
    subset2 = data.select(not_data_columns)

    # Clean the DataStream object
    result = clean_order(subset1)
    if result.is_err():
        return result.propagate()

    subset1 = result.unwrap()

    # Create DataStore from cleaned data
    ds = DataStore(subset1)

    # Recombine the data horizontally
    recombined_data = pl.concat([ds.as_ref(), subset2], how="horizontal")

    # Replace underlying data of ds with recombined_data
    _ = ds.copy_from(recombined_data)

    return Result.ok(ds)


def clean_new_data(new_data_stream: DataStream, ref: DataStore) -> Result[DataStore]:
    """Clean new student data for integration with existing registration data.

    Processes new student data through comprehensive cleaning pipeline to ensure
    compatibility with existing DataStore format and data quality standards.

    Args:
        new_data_stream (DataStream): Stream containing new student registration data.
        cohort (int): The cohort number from prexisting data

    Returns:
        Result[DataStore]: Success with cleaned DataStore ready for integration or error.
    """
    return _clean_new(new_data_stream, ref)
