from typing import NamedTuple

from pylms.constants import COHORT, TIMESTAMP_FMT
from pylms.utils import DataStore, date
from datetime import datetime


class UpdateFormDetails(NamedTuple):
    week_num: int
    year_num: int
    title: str
    name: str


def extract_update_details(ds: DataStore) -> UpdateFormDetails:
    cohort_no: int = ds.as_ref()[COHORT].iloc[0]
    week_num: int = date.det_week_num()
    year_num: int = date.det_year()
    timestamp: str = datetime.now().strftime(TIMESTAMP_FMT)
    form_title: str = f"Python Beginners Cohort {cohort_no} Registration Update Form"
    form_name: str = f"Cohort {cohort_no} Update {timestamp}"
    return UpdateFormDetails(
        title=form_title, name=form_name, week_num=week_num, year_num=year_num
    )
