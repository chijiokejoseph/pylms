import re
import pandas as pd
from pylms.utils.data import DataStream


def clean_col_names(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """
    Carries out formatting operations on the names of the columns contained in the underlying data of the input DataStream `data`. This cleaning operation involves several things
        - Renaming substrings matching "nysc" or "siwes" in the column names to upper case "NYSC" or "SIWES" as the case maybe
        - Removing trailing and leading whitespaces from the columns

    :param data_stream: (DataStream[pd.DataFrame]): DataStream object containing the data to be formatted
    :type: DataStream[pd.DataFrame]

    :rtype: DataStream [pd.DataFrame]
    :return: A DataStream object containing the formatted data
    """
    data: pd.DataFrame = data_stream().copy()
    for old_column in data.columns:
        new_column: str = old_column.strip().title()

        regex_nysc: re.Pattern = re.compile(r"nysc", flags=re.IGNORECASE)
        regex_siwes: re.Pattern = re.compile(r"siwes", flags=re.IGNORECASE)

        matches_nysc: list[str] | None = re.findall(regex_nysc, new_column)
        matches_siwes: list[str] | None = re.findall(regex_siwes, new_column)

        if matches_nysc:  # if matches_nysc is truthy i.e., is not None
            for each_match in matches_nysc:
                new_column = new_column.replace(each_match, each_match.upper())

        if matches_siwes:  # if matches_siwes is truthy i.e., is not None
            for each_match in matches_siwes:
                new_column = new_column.replace(each_match, each_match.upper())

        data[new_column] = data[old_column]
        # drop the old column if the new column name `new_column` is different from the old column name `old_column`
        data = data.drop(columns=old_column) if new_column != old_column else data

    new_data: DataStream[pd.DataFrame] = DataStream(data)
    return new_data
