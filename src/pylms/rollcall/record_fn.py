import pandas as pd

from ..constants import DATE, NAME
from ..data import DataStore, DataStream
from ..record import RecordStatus
from .names_filter import filter_names


def record(
    ds: DataStore, turnout_stream: DataStream[pd.DataFrame], fill_value: RecordStatus
) -> None:
    pretty: pd.DataFrame = ds.to_pretty()
    data_ref: pd.DataFrame = ds.as_ref()
    all_names = pretty.loc[:, NAME].astype(str)

    turnout_stream = filter_names(turnout_stream)
    turnout_data: pd.DataFrame = turnout_stream()
    present_names = turnout_data.loc[:, NAME].astype(str)
    class_date: str = turnout_data[DATE].iloc[0]

    class_record = data_ref.loc[:, class_date].astype(str)

    new_class_record = [
        str(fill_value) if each_name in present_names.tolist() else old_record
        for each_name, old_record in zip(all_names, class_record)
    ]
    data_ref.loc[:, class_date] = new_class_record
    return None
