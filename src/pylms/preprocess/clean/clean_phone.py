import pandas as pd
from pylms.constants import PHONE
from pylms.utils.data import DataStream
from pylms.preprocess.clean.re_phone import match_and_clean


def clean_phone(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """
    formats all the phone numbers in a pandas DataFrame or Series which is stored in the `data` argument. It converts international numbers to local format, and uses a semicolon as a delimiter.

    :param data_stream: ( DataStream[pd.DataFrame] ): A DataStream instance containing the data of phone numbers which are meant to be cleaned
    :type data_stream: DataStream[pd.DataFrame]

    :return: Formatted phone numbers as a DataStream object.
    :rtype: DataStream[pd.DataFrame]
    """

    def validate_data(test_data: pd.DataFrame) -> bool:
        """
        performs a series of validation operations on the `test_data` argument. These include
            - checking if the `test_data` contains a `PHONE` column
            - checking if the `test_data` does not contain any missing values
            - checking if the `test_data` contains only values of type `str`

        :param test_data: ( pd.DataFrame ): A dataframe object which is being validated
        :rtype: bool
        :return: a boolean that indicates if `test_data` is validated or not
        """

        # Test if `test_data` has a `PHONE` column
        test1: bool = PHONE in test_data.columns.tolist()
        if not test1:
            return False
        # Test if `test_data` does not contain any missing values
        test2_list: pd.Series[bool] = test_data[PHONE].notna()
        test2: bool = all(test2_list)
        if not test2:
            return False
        # Test that `test_data` only contains values of type `str`
        test3_list: pd.Series[bool] = test_data[PHONE].apply(
            lambda x: isinstance(x, str)
        )
        test3: bool = all(test3_list)
        return test3

    valid_data: pd.DataFrame = DataStream(data_stream(), validate_data)()
    valid_data[PHONE] = valid_data[PHONE].apply(match_and_clean)
    return DataStream(valid_data)
