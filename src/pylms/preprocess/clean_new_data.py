import pandas as pd

from ..clean import (
    clean_cohort,
    clean_completion_date,
    clean_date,
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
from ..constants import DATA_COLUMNS, NAME, PHONE
from ..data import DataStore, DataStream
from ..errors import Result


def _clean_new(data_stream: DataStream[pd.DataFrame]) -> Result[DataStore]:
    def validate_na_removal(test_data: pd.DataFrame) -> bool:
        return not test_data.isna().any().any()

    result = clean_na(data_stream, validate_na_removal)
    if result.is_err():
        return result.propagate()

    clean_str(data_stream, [NAME, PHONE])
    clean_email(data_stream)
    clean_name(data_stream)

    result = clean_phone(data_stream)
    if result.is_err():
        return result.propagate()

    result = clean_cohort(data_stream)
    if result.is_err():
        return result.propagate()

    result = clean_date(data_stream)
    if result.is_err():
        return result.propagate()

    clean_time(data_stream)
    clean_internship(data_stream)
    clean_training(data_stream)

    result = clean_completion_date(data_stream)
    if result.is_err():
        return result.propagate()

    clean_duplicates(data_stream)
    clean_sort(data_stream)

    # get list of columns in `data_stream`
    columns: list[str] = data_stream().columns.tolist()
    # get list of columns in `data_stream` that are not in `DATA_COLUMNS`
    not_data_columns: list[str] = [
        column for column in columns if column not in DATA_COLUMNS
    ]
    # get list of columns in `data_stream` that are in `DATA_COLUMNS`
    data_columns: list[str] = [column for column in columns if column in DATA_COLUMNS]

    # extract the dataframe for only columns in `DATA_COLUMNS`
    subset1 = data_stream.as_ref()[data_columns]
    # extract the dataframe for only columns not in `DATA_COLUMNS`
    subset2 = data_stream.as_ref()[not_data_columns]

    # clean that DataStream object
    result = clean_order(DataStream(subset1))
    if result.is_err():
        return result.propagate()

    subset1 = result.unwrap()

    # create a DataStore from the cleaned data
    ds: DataStore = DataStore(subset1)

    # recombine the data in the DataStore and the data corresponding to columns not in `DATA_COLUMNS`
    recombined_data = pd.concat([ds.as_ref(), subset2], axis="columns")

    # use a setter to replace the underlying data of `ds` with `recombined_data`
    ds.data = recombined_data

    return Result.ok(ds)


def clean_new_data(new_data_stream: DataStream[pd.DataFrame]) -> Result[DataStore]:
    """
    cleans data that is passed into the program to add additional entries to the main registration data which has already been stored as a `DataStore` object.

    :param new_data_stream: (DataStream[pd.DataFrame]): A `DataStream` object that contains an underlying pandas DataFrame. it is the data read into the program to add extra entries to the already processed registration data.
    :type new_data_stream: DataStream[pd.DataFrame]

    :return: (Result[DataStore]) - a `Result` containing the `DataStore` object of the cleaned data, which makes it suitable for being added to the existing registration data that is also stored as a `DataStore`.
    :rtype: Result[DataStore]
    """
    return _clean_new(new_data_stream)
