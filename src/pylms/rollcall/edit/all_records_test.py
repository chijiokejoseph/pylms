import unittest
from pylms.data_ops import load
from pylms.record import RecordStatus
from pylms.rollcall import GlobalRecord
from pylms.utils import date
from pylms.rollcall.edit.input_dates import input_date_for_edit
from pylms.rollcall.edit.all_records import edit_all_records
from pylms.rollcall.edit.edit_type import EditType
import time
import pandas as pd
from pylms.history import History

class EditAllTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ds = load()
        self.history = History.load()

    def test_edit_all(self) -> None:
        print("Select the last date for this test\n\n")
        print("Select the Global Attendance Record as PRESENT.")
        time.sleep(1)
        input_dates: list[str] = input_date_for_edit(self.history, EditType.ALL).unwrap()
        edit_all_records(self.ds, input_dates)
        all_dates = date.retrieve_dates("all")
        last_date = all_dates[-1]
        record = GlobalRecord().dates.get(last_date)
        self.assertEqual(record, RecordStatus.PRESENT)  # add assertion here
        cond: pd.Series = self.ds.as_ref().loc[:, last_date] == RecordStatus.PRESENT
        self.assertTrue(cond.all())


if __name__ == "__main__":
    unittest.main()
