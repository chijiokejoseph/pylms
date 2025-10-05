import unittest

from pylms.preprocess.clean_pipeline.clean_reg_data import _clean_reg
from pylms.utils import read_data, DataStream
import pandas as pd
from pathlib import Path


class CleanRegTest(unittest.TestCase):
    def setUp(self) -> None:
        self.path: Path = Path(
            r"C:\Users\chijioke joseph\OneDrive\NCAIR\Cohorts\Cohort 25\Attendance\Registration.xlsx"
        )

    def test_clean_reg(self) -> None:
        data = read_data(self.path)
        data_stream = DataStream[pd.DataFrame](data)
        ds_result = _clean_reg(data_stream)
        assert ds_result.is_ok()
        ds = ds_result.unwrap()
        print(ds.as_ref())
