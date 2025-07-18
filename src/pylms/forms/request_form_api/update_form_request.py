import json
from pathlib import Path

from pylms.forms.request_form_api.update_form_init import init_update_form
from pylms.forms.request_form_api.utils import UpdateFormInfo
from pylms.utils import DataStore, paths


def request_update_form(ds: DataStore) -> None:
    update_form_path: Path = paths.get_update_path("form")

    if update_form_path.exists():
        with open(update_form_path, "r", encoding="utf-8") as file:
            data_dict = json.load(file)
            data_form: UpdateFormInfo = UpdateFormInfo(**data_dict)
            print(
                f"\nRegistration Update Form already generated for this week, Week {data_form.week_num} of Year {data_form.year_num}\n. Only one Registration Update Form can be generated for each cohort.\n"
            )
            print(
                f"\nRegistration Update Form Url for Week {data_form.week_num} of Year {data_form.year_num}: {data_form.url}\n"
            )
            print(f"\nClass Dates included in the form: {data_form.dates}\n")
    else:
        init_update_form(ds)
