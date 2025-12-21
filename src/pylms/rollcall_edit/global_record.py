import json
from pathlib import Path
from typing import NamedTuple, Self, final

from ..constants import GLOBAL_RECORD_PATH
from ..data import DataStore
from ..errors import Result, eprint
from ..paths import get_global_record_path, get_paths_json
from ..record import RecordStatus, retrieve_record


class _DateRecord(NamedTuple):
    dates: dict[str, RecordStatus]

    def swap(self, target_date: str, new_record: RecordStatus) -> None:
        if self.dates.get(target_date) is None:
            return None
        self.dates[target_date] = new_record
        return None

    def unwrap(
        self, target_date: str, new_record: RecordStatus
    ) -> Result[RecordStatus]:
        if self.dates.get(target_date) is None:
            msg = f"Entry {target_date} not found among dates list"
            eprint(msg)
            return Result.err(msg)
        if self.dates[target_date] != RecordStatus.EMPTY:
            value = self.dates[target_date]
            return Result.ok(value)
        return Result.ok(new_record)


@final
class GlobalRecord:
    date_record: _DateRecord

    def __init__(self) -> None:
        self.date_record = _DateRecord({})
        pass

    @classmethod
    def new(cls) -> Result[Self]:
        instance = cls()
        global_record_path: Path = get_global_record_path()
        if global_record_path.exists():
            with global_record_path.open("r") as file_record:
                data = json.load(file_record)
                record: dict[str, RecordStatus] = {
                    key: retrieve_record(value) for key, value in data.items()
                }
                instance.date_record = _DateRecord(record)
                return Result.ok(instance)

        if not get_paths_json()["Date"].exists():
            msg = f"The save path for dates: {get_paths_json()['Date'].absolute()} does not exist"
            eprint(msg)
            return Result.err(msg)

        with get_paths_json()["Date"].open("r") as file_record:
            dates_list: list[str] = json.load(file_record)
            instance.date_record = _DateRecord(
                {date: RecordStatus.EMPTY for date in dates_list}
            )

        return Result.ok(instance)

    @property
    def dates(self) -> dict[str, RecordStatus]:
        return self.date_record.dates

    def swap(self, target_date: str, new_record: RecordStatus) -> None:
        self.date_record.swap(target_date, new_record)
        save_data: dict[str, str] = {
            key: str(value) for key, value in self.dates.items()
        }

        global_record_path: Path = get_global_record_path()

        with global_record_path.open("w") as file:
            json.dump(save_data, file)

        with GLOBAL_RECORD_PATH.open("w") as file:
            json.dump(save_data, file)

    def unwrap(
        self, target_date: str, new_record: RecordStatus
    ) -> Result[RecordStatus]:
        return self.date_record.unwrap(target_date, new_record)

    def crosscheck(self, ds: DataStore) -> None:
        data_ref = ds.as_ref()
        for target_date, value in self.dates.items():
            if value != RecordStatus.EMPTY:
                data_ref.loc[:, target_date] = value
        return None

    def retrieve_unset_dates(self) -> list[str]:
        return [
            date for date, value in self.dates.items() if value == RecordStatus.EMPTY
        ]
