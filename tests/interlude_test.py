import unittest
from datetime import datetime
from typing import override
from unittest.case import TestCase

from pylms.cli import get_interlude_dates
from pylms.constants import DATA_COLUMNS, DATE_FMT, DEFAULT_DATA_PATH
from pylms.data import DataStore
from pylms.data_service import load
from pylms.history import (
    History,
    Interlude,
    add_interlude,
    all_dates,
    load_history,
    save_history,
    sync_classes,
)


class TestClass(TestCase):
    history: History
    ds: DataStore

    def __init__(self, method_name: str) -> None:
        self.history = load_history().unwrap()
        self.ds = load().unwrap()
        super().__init__(methodName=method_name)

    @override
    def setUp(self) -> None:
        self.history = load_history().unwrap()
        return super().setUp()

    def test_sync_classes(self) -> None:
        start = self.history.dates[4]
        end = datetime.strptime("05/01/2026", DATE_FMT)

        interlude = Interlude.new(start, end).unwrap()

        self.history.interlude = interlude

        _ = sync_classes(self.history).unwrap()

        dates = all_dates(self.history, "")

        for i, date in enumerate(dates, start=1):
            print(f"{str(i):<2}. {date}")

    def test_add_interlude(self) -> None:
        interlude = get_interlude_dates(self.history).unwrap()
        _ = add_interlude(self.ds, self.history, interlude).unwrap()

        dates = all_dates(self.history, "")

        for i, date in enumerate(dates, start=1):
            print(f"{str(i):<2}. {date}")

        date_cols = [
            col for col in self.ds.as_ref().columns.tolist() if col not in DATA_COLUMNS
        ]

        for col in date_cols:
            print(f"{col = }")

        _ = save_history(self.history).unwrap()

        _ = self.ds.to_excel(DEFAULT_DATA_PATH / "interlude_test.xlsx").unwrap()


if __name__ == "__main__":
    _ = unittest.main()
