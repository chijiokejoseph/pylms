from typing import NamedTuple

from pylms.constants import COHORT
from pylms.utils import DataStore, date


class UpdateFormDetails(NamedTuple):
    week_num: int
    year_num: int
    title: str
    name: str


def scrape_update_form(ds: DataStore) -> UpdateFormDetails:
    cohort_no: int = ds()[COHORT].iloc[0]
    week_num: int = date.det_week_num()
    year_num: int = date.det_year()
    form_name: str = f"Registration Week {week_num} Year {year_num}"
    form_title: str = f"Python Beginners Cohort {cohort_no} Registration Update Week {week_num} of Year {year_num}"
    return UpdateFormDetails(
        title=form_title, name=form_name, week_num=week_num, year_num=year_num
    )
