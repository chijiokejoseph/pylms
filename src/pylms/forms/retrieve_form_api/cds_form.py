from pathlib import Path
from typing import cast

import pandas as pd

from pylms.errors import Result
from pylms.models import CDSFormInfo
from pylms.forms.utils import select_form
from pylms.forms.retrieve_form_api.form import retrieve_form
from pylms.history import History
from pylms.models.form_info import UpdateFormInfo
from pylms.utils import DataStream, paths


def retrieve_cds_form(
    history: History,
) -> Result[tuple[DataStream[pd.DataFrame] | None, CDSFormInfo]]:
    form_info: Result[CDSFormInfo | UpdateFormInfo] = select_form(history, "cds")
    if form_info.is_err():
        return Result[tuple[DataStream[pd.DataFrame] | None, CDSFormInfo]].err(form_info.unwrap_err())
    info: CDSFormInfo = cast(CDSFormInfo, form_info.unwrap())
    cds_form_path: Path = paths.get_cds_path("form", info.timestamp)
    cds_record_path: Path = paths.get_cds_path("record", info.timestamp)
    result = retrieve_form(cds_form_path, cds_record_path, CDSFormInfo), info
    return Result[tuple[DataStream[pd.DataFrame] | None, CDSFormInfo]].ok(result)
