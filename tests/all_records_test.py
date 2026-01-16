import time
import unittest
from typing import final, override

import pandas as pd

from pylms.data_service import load
from pylms.history import load_history, retrieve_dates
from pylms.record import RecordStatus
from pylms.rollcall_edit import (
    edit_all_records,
    input_date_for_edit,
)


@final
class EditAllTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.ds = load().unwrap()  # pyright: ignore[reportUninitializedInstanceVariable]
        self.history = load_history().unwrap()  # pyright: ignore[reportUninitializedInstanceVariable]

    def test_edit_all(self) -> None:
        ds = self.ds
        history = self.history
        print("Select the last date for this test\n\n")
        print("Select the Global Attendance Record as PRESENT.")

        time.sleep(1)

        input_dates: list[str] = input_date_for_edit(history).unwrap()
        _ = edit_all_records(ds, history, input_dates).unwrap()

        all_dates = retrieve_dates("").unwrap()

        last_date = all_dates[-1]

        cond: pd.Series = ds.as_ref().loc[:, last_date] == RecordStatus.PRESENT
        self.assertTrue(cond.all())


if __name__ == "__main__":
    _ = unittest.main()
