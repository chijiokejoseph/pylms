from pathlib import Path

import pandas as pd

from pylms.forms.request_form_api import CDSFormInfo
from pylms.forms.retrieve_form_api.form import retrieve_form
from pylms.utils import DataStream, paths


def retrieve_cds_form() -> DataStream[pd.DataFrame] | None:
    cds_form_path: Path = paths.get_cds_path("form")
    cds_record_path: Path = paths.get_cds_path("record")
    return retrieve_form(cds_form_path, cds_record_path, CDSFormInfo)
