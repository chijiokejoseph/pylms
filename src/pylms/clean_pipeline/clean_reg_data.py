from pathlib import Path

import pandas as pd

from pylms.cli import input_path, test_path_in
from pylms.constants import NAME, PHONE
from pylms.utils import DataStore, DataStream, clean, read_data


def _clean_reg(data_stream: DataStream[pd.DataFrame]) -> DataStore:
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



    :param data_stream: (DataStream[pd.DataFrame]): registration data passed in as a `DataStream` Object.
    :type data_stream: DataStream[pd.DataFrame]

    :return: a preprocessed `DataStore` object
    :rtype: DataStore
    """
    data_stream = clean.clean_col_names(data_stream)
    data_stream = clean.clean_columns(data_stream)
    data_stream = clean.clean_na(data_stream)
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
    data_stream = clean.clean_order(data_stream)
    return DataStore(data_stream())


def clean_reg_data() -> DataStore:
    """
    This function takes no arguments and prompts the user to enter certain metadata that confirm that all the requirements for preprocessing a new registration data are met. Please see `cli.input_cleaning_req` for more details.

    After this, the function tries to read data from a `Registration.xlsx` file that has been created by the user in the directory `data` which is a direct child of the project root using the `read_data` function from the utility `utils.data.read_data`. Upon successfully reading the data, the data is converted to a `DataStream` and then cleaned using the private utility function `_clean_reg` and returned as a `DataStore`.

    :return: a `DataStore` object holding the cleaned data from the new registration data
    :rtype: DataStore
    """

    msg: str = """Enter the absolute path to the new cohort spreadsheet for the students.
Enter the path:  """

    register_path: Path = input_path(
        msg,
        path_test_fn=test_path_in,
        path_test_diagnosis="The path entered does not exist, "
        "is not absolute or is not a valid excel file.",
    )
    dataframe: pd.DataFrame = read_data(register_path)
    register_ds: DataStream[pd.DataFrame] = DataStream(dataframe)
    return _clean_reg(register_ds)
