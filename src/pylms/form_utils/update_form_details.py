from datetime import datetime
from typing import NamedTuple

from ..constants import COHORT, TIMESTAMP_FMT
from ..data import DataStore
from ..date import det_week_num, det_year


class UpdateFormDetails(NamedTuple):
    """Named tuple containing update form details."""
    week_num: int
    year_num: int
    title: str
    name: str
    timestamp: str


def extract_update_details(ds: DataStore) -> UpdateFormDetails:
    """Extract details needed for creating update form.
    
    Args:
        ds (DataStore): DataStore containing cohort information.
        
    Returns:
        UpdateFormDetails: Named tuple with form title, name, and timing details.
    """
    cohort_no: int = ds.as_ref()[0, COHORT]
    week_num: int = det_week_num()
    year_num: int = det_year()
    timestamp: str = datetime.now().strftime(TIMESTAMP_FMT)
    form_title: str = f"Python Beginners Cohort {cohort_no} Registration Update Form"
    form_name: str = f"Cohort {cohort_no} Update {timestamp}"
    
    return UpdateFormDetails(
        title=form_title,
        name=form_name,
        week_num=week_num,
        year_num=year_num,
        timestamp=timestamp,
    )
