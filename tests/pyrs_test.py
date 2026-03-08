import re
import unittest
from typing import final, override
from unittest import TestCase

import polars as pl

from pylms.clean.rclean import clean_dates, clean_names
from pylms.constants import DATA_PATH
from pylms.data import read


@final
class TestPyrs(TestCase):
    data: pl.DataFrame | None = None

    @override
    def setUp(self) -> None:
        reg_path = DATA_PATH / "Registration.xlsx"
        self.data = read(reg_path).unwrap()

    def test_clean_name(self) -> None:
        assert self.data is not None
        data = self.data
        reg = re.compile("(?i)name")
        name_col = [col for col in data.columns if reg.match(col) is not None]
        if len(name_col) == 1:
            name = name_col[0]
        else:
            raise ValueError("issue with getting name column")
        data = data.select(pl.col(name))
        print(f"Before Data\n{data}\n")
        data = data.select(pl.col(name).map_batches(clean_names).alias("Cleaned Name"))
        print(f"After Data\n{data}\n")

    def test_clean_date(self) -> None:
        assert self.data is not None
        data = self.data
        date_col = [
            col for col in data.columns if re.compile("(?i)date").match(col) is not None
        ]
        if len(date_col) == 1:
            date = date_col[0]
        else:
            raise ValueError("issue with getting date column")

        data = data.select(pl.col(date).dt.strftime("%d/%m/%Y").alias(date))
        print(f"Before Data\n{data}\n")

        format = "%d/%m/%Y"
        day_first = False

        def clean_dates_util(dates: pl.Series) -> pl.Series:
            return clean_dates(dates, format, day_first)

        data = data.with_columns(pl.col(date).map_batches(clean_dates_util))
        print(f"After Data\n{data}\n")


if __name__ == "__main__":
    _ = unittest.main()
