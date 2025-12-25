import pandas as pd

from ..data import DataStream
from ..errors import Result
from ..form_utils import select_form
from ..history import History
from ..models import CDSFormInfo
from .form import retrieve_form


def retrieve_cds_form(
    history: History,
) -> Result[tuple[DataStream[pd.DataFrame], CDSFormInfo]]:
    info = select_form(history, "cds")

    if info.is_err():
        return info.propagate()

    info = info.unwrap()

    cds_form = retrieve_form(info)

    if cds_form.is_err():
        return cds_form.propagate()

    cds_form = cds_form.unwrap()

    return Result.ok((cds_form, info))
