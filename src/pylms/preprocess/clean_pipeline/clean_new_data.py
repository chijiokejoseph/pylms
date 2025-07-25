import pandas as pd
from pylms.constants import PHONE, NAME, DATA_COLUMNS
from pylms.utils import DataStream, DataStore, data
from pylms.preprocess import clean

read_data = data.read_data


def _clean_new(data_stream: DataStream[pd.DataFrame]) -> DataStore:
    def validate_na_removal(test_data: pd.DataFrame) -> bool:
        return not test_data.isna().any().any()

    data_stream = clean.clean_na(data_stream, validate_na_removal)
    data_stream = clean.clean_str(data_stream, [NAME, PHONE])
    data_stream = clean.clean_email(data_stream)
    data_stream = clean.clean_name(data_stream)
    data_stream = clean.clean_phone(data_stream)
    data_stream = clean.clean_cohort(data_stream)
    data_stream = clean.clean_date(data_stream)
    data_stream = clean.clean_time(data_stream)
    data_stream = clean.clean_internship(data_stream)
    data_stream = clean.clean_training(data_stream)
    data_stream = clean.clean_completion_date(data_stream)
    data_stream = clean.clean_duplicates(data_stream)
    data_stream = clean.clean_sort(data_stream)

    # get list of columns in `data_stream`
    columns: list[str] = data_stream().columns.tolist()
    # get list of columns in `data_stream` that are not in `DATA_COLUMNS`
    not_data_columns: list[str] = [
        column for column in columns if column not in DATA_COLUMNS
    ]
    # get list of columns in `data_stream` that are in `DATA_COLUMNS`
    data_columns: list[str] = [column for column in columns if column in DATA_COLUMNS]

    # extract the dataframe for only columns in `DATA_COLUMNS`
    subset1_data = data_stream()[data_columns]
    # extract the dataframe for only columns not in `DATA_COLUMNS`
    subset2_data = data_stream()[not_data_columns]

    # create a DataStream object of the data with columns in `DATA_COLUMNS`
    subset1_ds: DataStream[pd.DataFrame] = DataStream(subset1_data)
    # clean that DataStream object
    subset1_ds = clean.clean_order(subset1_ds)

    # create a DataStore from the cleaned data
    ds: DataStore = DataStore(subset1_ds.as_ref())
    # recombine the data in the DataStore and the data corresponding to columns not in `DATA_COLUMNS`
    recombined_data = pd.concat([ds.as_ref(), subset2_data], axis="columns")
    # use a setter to replace the underlying data of `ds` with `recombined_data`
    ds.data = recombined_data

    return ds


def clean_new_data(new_data_stream: DataStream[pd.DataFrame]) -> DataStore:
    """
    cleans data that is passed into the program to add additional entries to the main registration data which has already been stored as a `DataStore` object.

    :param new_data_stream: (DataStream[pd.DataFrame]): A `DataStream` object that contains an underlying pandas DataFrame. it is the data read into the program to add extra entries to the already processed registration data.
    :type new_data_stream: DataStream[pd.DataFrame]

    :return: a `DataStore` object of the cleaned data, which makes it suitable for being added to the existing registration data that is also stored as a `DataStore`.
    :rtype: DataStore
    """
    return _clean_new(new_data_stream)
