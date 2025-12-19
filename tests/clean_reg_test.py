import unittest
from pathlib import Path
from typing import override

from pylms.data import DataStream, read
from pylms.preprocess import clean_reg


class CleanRegTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.path: Path = (  # pyright: ignore [reportUninitializedInstanceVariable]
            Path.home()
            / r"OneDrive\NCAIR\Cohorts\Cohort 31\Documents\Registration.xlsx"
        )

    def test_clean_reg(self) -> None:
        data = read(self.path)
        assert data.is_ok()
        data = data.unwrap()
        data_stream = DataStream(data)
        ds_result = clean_reg(data_stream)
        assert ds_result.is_ok()
        ds = ds_result.unwrap()
        print(ds.as_ref())


if __name__ == "__main__":
    print("I am hungry")
    _ = unittest.main()
