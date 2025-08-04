import unittest
from datetime import datetime
from pylms.utils.date.det_date_features import retrieve_dates, to_unique_week_nums, to_week_num, to_week_nums
from pylms.constants import DATE_FMT


class DetDateTest(unittest.TestCase):
    def test_det_date(self) -> None:
        dates_list: list[str] = retrieve_dates()
        unique_week_nums: list[int] = to_unique_week_nums(dates_list)
        last_date: str = dates_list[-1]
        last_datetime: datetime = datetime.strptime(last_date, DATE_FMT)
        print(f"{last_datetime = }")
        print(f"{last_datetime.isocalendar() = }")
        print(f"{last_datetime.isocalendar().week = }")
        print(f"{unique_week_nums = }")
        print(f"{to_week_num(last_date) = }")
        print(f"{to_week_nums(dates_list) = }")
