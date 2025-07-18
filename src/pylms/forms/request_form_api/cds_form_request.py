import json
from pathlib import Path

from pylms.constants import COHORT
from pylms.forms.request_form_api.cds_form_init import init_cds_form
from pylms.forms.request_form_api.utils import CDSFormInfo
from pylms.utils import DataStore, date, paths


def request_cds_form(ds: DataStore) -> None:
    cds_form_path: Path = paths.get_paths_json()["CDSForm"]
    dates_list: list[str] = date.retrieve_dates()
    unique_week_nums: tuple[int, ...] = date.to_unique_week_nums(dates_list)
    week_num: int = date.det_week_num()
    cohort_no: int = ds()[COHORT].iloc[0]

    start_date: str = dates_list[0]
    cds_week: int = unique_week_nums[1]
    start_week: int = unique_week_nums[0]

    if week_num != cds_week:
        print(
            f"CDS Form can only be created on the second week of the cohort.\nThe current cohort is {cohort_no} which kicked off at {start_date}, week {start_week}. \nHence CDS Form can only be generated at week {cds_week}, yet the current week is week {week_num}"
        )
        return None

    if cds_form_path.exists():
        with open(cds_form_path, "r", encoding="utf-8") as file:
            data_dict = json.load(file)
            cds_form: CDSFormInfo = CDSFormInfo(**data_dict)
            print(
                f"CDS Form already generated for this cohort, Week {cds_week} of Year {date.det_year()}. \nOnly one CDS Entry Form can be generated for each cohort."
            )
            print(
                f"CDS Form Url for Week {cds_week} of Year {date.det_year()}: {cds_form.url}"
            )
            return None
    else:
        init_cds_form(ds)
        return None
