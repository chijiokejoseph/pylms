# pyright: reportUninitializedInstanceVariable=false
import unittest
from datetime import datetime
from typing import final, override
from unittest.case import TestCase

from pylms.config import Config, init_config
from pylms.constants import DATA_COLUMNS, DATA_PATH, DATE_FMT
from pylms.data import DataStore
from pylms.data_service import init_ds
from pylms.history import (
    History,
    Interlude,
    add_interlude,
    all_dates,
    init_history,
    new_interlude,
    save_history,
    sync_classes,
)


@final
class TestClass(TestCase):
    config: Config
    history: History
    ds: DataStore

    @override
    def setUp(self) -> None:
        self.config = init_config().unwrap()
        self.history = init_history(self.config).unwrap()
        self.ds = init_ds(self.config, self.history).unwrap()
        super().setUp()

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
        interlude = new_interlude(self.history).unwrap()
        _ = add_interlude(self.ds, self.history, interlude).unwrap()

        dates = all_dates(self.history, "")

        for i, date in enumerate(dates, start=1):
            print(f"{str(i):<2}. {date}")

        date_cols = [col for col in self.ds.as_ref().columns if col not in DATA_COLUMNS]

        for col in date_cols:
            print(f"{col = }")

        _ = save_history(self.config, self.history).unwrap()

        _ = self.ds.write(DATA_PATH / "interlude_test.xlsx").unwrap()


if __name__ == "__main__":
    _ = unittest.main()
