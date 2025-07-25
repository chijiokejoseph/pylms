import pandas as pd

from pylms.constants import DATE, NAME
from pylms.record import RecordStatus
from pylms.rollcall.record.names_filter import filter_names
from pylms.utils import DataStore, DataStream


def record(
    ds: DataStore, turnout_stream: DataStream[pd.DataFrame], fill_value: RecordStatus
) -> DataStore:
    pretty_data: pd.DataFrame = ds.pretty()
    data_ref: pd.DataFrame = ds.as_ref()
    all_names: list[str] = pretty_data[NAME].tolist()

    turnout_stream = filter_names(turnout_stream)
    turnout_data: pd.DataFrame = turnout_stream()
    present_names: list[str] = turnout_data[NAME].tolist()
    class_date: str = turnout_data[DATE].iloc[0]

    class_record: list[str] = data_ref[class_date].tolist()

    new_class_record: list[str] = [
        fill_value if each_name in present_names else old_record
        for each_name, old_record in zip(all_names, class_record)
    ]
    data_ref[class_date] = new_class_record
    return ds
