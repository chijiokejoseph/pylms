from pathlib import Path
from typing import cast

import pandas as pd

from pylms.models import CDSFormInfo
from pylms.forms.utils import select_form
from pylms.forms.retrieve_form_api.form import retrieve_form
from pylms.state import History
from pylms.utils import DataStream, paths


def retrieve_cds_form(
    history: History,
) -> tuple[DataStream[pd.DataFrame] | None, CDSFormInfo]:
    info: CDSFormInfo = cast(CDSFormInfo, select_form(history, "cds"))
    cds_form_path: Path = paths.get_cds_path("form", info.timestamp)
    cds_record_path: Path = paths.get_cds_path("record", info.timestamp)
    return retrieve_form(cds_form_path, cds_record_path, CDSFormInfo), info
