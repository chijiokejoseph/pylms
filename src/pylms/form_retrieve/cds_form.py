from pathlib import Path
from typing import cast

import pandas as pd

from ..data import DataStream
from ..errors import Result
from ..form_utils import select_form
from ..history import History
from ..models import CDSFormInfo
from ..paths import get_cds_path
from .form import retrieve_form


def retrieve_cds_form(
    history: History,
) -> Result[tuple[DataStream[pd.DataFrame], CDSFormInfo]]:
    form_info = select_form(history, "cds")

    if form_info.is_err():
        return form_info.propagate()

    info: CDSFormInfo = cast(CDSFormInfo, form_info.unwrap())
    cds_form_path: Path = get_cds_path("form", info.timestamp)
    cds_record_path: Path = get_cds_path("record", info.timestamp)

    cds_form = retrieve_form(cds_form_path, cds_record_path, CDSFormInfo)

    if cds_form.is_err():
        return cds_form.propagate()

    cds_form = cds_form.unwrap()

    return Result.ok((cds_form, info))
