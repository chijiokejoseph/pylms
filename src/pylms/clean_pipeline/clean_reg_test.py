import unittest

from pylms.clean_pipeline.clean_reg_data import _clean_reg
from pylms.utils import read_data, DataStream
import pandas as pd
from pathlib import Path


class CleanRegTest(unittest.TestCase):
    def setUp(self) -> None:
        self.path: Path = Path(
            r"C:\Users\chijioke joseph\OneDrive\Documents - Local\NCAIR\25th Cohort\Attendance\Registration.xlsx"
        )

    def test_clean_reg(self) -> None:
        data = read_data(self.path)
        data_stream = DataStream[pd.DataFrame](data)
        ds = _clean_reg(data_stream)
        print(ds())
