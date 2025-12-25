from pathlib import Path

import pandas as pd

from ..clean import (
    clean_cohort,
    clean_col_names,
    clean_columns,
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
from ..cli import input_path
from ..constants import NAME, PHONE
from ..data import DataStore, DataStream, read
from ..errors import Result


def clean_reg(data_stream: DataStream[pd.DataFrame]) -> Result[DataStore]:
    """
    private helper function that carries out the actual cleaning operation on the registration data that is passed in as a `DataStream` object containing and underlying pandas DataFrame. After cleaning the data, the data is returned back as a `DataStore`.

    The following cleaning operations are carried out on the data passed in as the argument to `data_stream`.

        - Renaming the Columns to suitable names i.e., removing any trailing or leading whitespace in the columns.
        - Removing duplicate entries in the data. See `utils.clean.clean_duplicates` for more info about this process.
        - Removing unwanted columns from the data. See `utils.clean.clean_columns` for more info about this process.
        - Removing NaN / missing values from the data. See `utils.clean.clean_na` for more info about this process.
        - Checking columns that are meant to hold str data but may be parsed by pandas as numbers to convert any such mistyped value to a suitable str. In essence, a string column like `Phone Number` is well known to have its values misinterpreted as numbers, this function checks for such problematic values and fixes them. See `utils.clean.clean_str` for more details.
        - Lowercasing and stripping all email entries in the data
        - Formatting and stripping all name entries in the data. To learn more about this formatting, see `utils.clean.clean_name` for more info.
        - Formatting and stripping all phone number entries in the data. To learn more about this formatting, see `utils.clean.clean_phone` and `utils.clean.re_phone` package for more info.
        - Replaces all the cohort entries with a single number value which is gotten from the user. Since the column Cohort is supposed to contain the same values, the single value entered from the user suffices.
        - Replaces all the date entries with a single date string entered by the user. Since the date entry records the orientation date of the cohort, its value is supposed to remain unchanged for each observation, hence a single value entered by the user suffices.
        - Replaces all the entries in the column `TRAINING` with a constant defined in the code. See `utils.clean.clean_training` for more info.
        - Formats the completion dates specified in the column `COMPLETION` are formatted as yyyy/mm/dd. See `utils.clean.clean_completion_date` for more info.
        - Sorts the data entries using the names from the registration data. The names are sorted in alphabetical order, and its indices are reset. An extra column called "S/N" is added to the data and just counts from 1 to the last entry in the data. Then finally, the columns of the data are reordered to match the same ordering in the list `DATA_COLUMNS` which can be seen in the `constants.py` file from the main working directory.



    :param data_stream: (Result[DataStream[pd.DataFrame]]): A result containing the registration data passed in as a `DataStream` Object.
    :type data_stream: Result[DataStream[pd.DataFrame]]

    :return: a preprocessed `DataStore` object
    :rtype: DataStore
    """
    clean_col_names(data_stream)
    clean_columns(data_stream)

    result = clean_na(data_stream)
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

    result = clean_order(data_stream)
    if result.is_err():
        return result.propagate()

    data_stream = result.unwrap()

    return Result.ok(DataStore(data_stream))


def clean_reg_data() -> Result[DataStore]:
    """
    This function prompts the user to enter the path to the registration excel spreadsheet file. Reads it and preprocesses it to a DataStore.

    :return: a result object of generic type `DataStore` holding the cleaned data from the new registration data
    :rtype: Result[DataStore]
    """

    msg: str = """Enter the absolute path to the new cohort spreadsheet for the students.
Enter the path:  """

    result = input_path(
        msg,
    )
    if result.is_err():
        return result.propagate()
    register_path: Path = result.unwrap()
    dataframe = read(register_path)
    if dataframe.is_err():
        return dataframe.propagate()
    dataframe = dataframe.unwrap()
    register_ds: DataStream[pd.DataFrame] = DataStream(dataframe)
    return clean_reg(register_ds)
