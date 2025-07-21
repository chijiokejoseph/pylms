from typing import NamedTuple
from pylms.errors import LMSError
from pylms.record import RecordStatus, retrieve_record
from pylms.constants import GLOBAL_RECORD_PATH
from pathlib import Path
import json

from pylms.rollcall.errors import PathNotFoundError
from pylms.utils import DataStore, paths


class _DateRecord(NamedTuple):
    dates: dict[str, RecordStatus]

    def swap(self, target_date: str, new_record: RecordStatus) -> None:
        if self.dates.get(target_date) is None:
            return None
        self.dates[target_date] = new_record
        return None

    def unwrap(self, target_date: str, new_record: RecordStatus) -> RecordStatus:
        if self.dates.get(target_date) is None:
            raise LMSError(f"Entry {target_date} not found among dates list")
        if self.dates[target_date] != RecordStatus.EMPTY:
            return self.dates[target_date]
        return new_record


class GlobalRecord:
    def __init__(self) -> None:
        global_record_path: Path = paths.get_global_record_path()
        if global_record_path.exists():
            with global_record_path.open("r") as file_record:
                data = json.load(file_record)
                record: dict[str, RecordStatus] = {
                    key: retrieve_record(value) for key, value in data.items()
                }
                self.date_record: _DateRecord = _DateRecord(record)
                return

        if not paths.get_paths_json()["Date"].exists():
            raise PathNotFoundError(
                f"The save path for dates: {paths.get_paths_json()['Date'].absolute()} does not exist"
            )
        with paths.get_paths_json()["Date"].open("r") as file_record:
            dates_list: list[str] = json.load(file_record)
            self.date_record = _DateRecord(
                {date: RecordStatus.EMPTY for date in dates_list}
            )

    @property
    def dates(self) -> dict[str, RecordStatus]:
        return self.date_record.dates

    def swap(self, target_date: str, new_record: RecordStatus) -> None:
        self.date_record.swap(target_date, new_record)
        save_data: dict[str, str] = {
            key: str(value) for key, value in self.dates.items()
        }
        
        global_record_path: Path = paths.get_global_record_path()
        
        with global_record_path.open("w") as file:
            json.dump(save_data, file)

        with GLOBAL_RECORD_PATH.open("w") as file:
            json.dump(save_data, file)

    def unwrap(self, target_date: str, new_record: RecordStatus) -> RecordStatus:
        return self.date_record.unwrap(target_date, new_record)

    def crosscheck(self, ds: DataStore) -> DataStore:
        data = ds()
        for target_date, value in self.dates.items():
            if value != RecordStatus.EMPTY:
                data.loc[:, target_date] = value
        ds.data = data
        return ds
