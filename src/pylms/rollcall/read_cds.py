import pandas as pd

from ..constants import CDS, NAME
from ..data import DataStream


def extract_cds(
    data_form_stream: DataStream[pd.DataFrame],
) -> tuple[DataStream[pd.DataFrame], DataStream[pd.DataFrame]]:
    data: pd.DataFrame = data_form_stream()
    new_data = data.copy()
    cds_data: pd.DataFrame = new_data.loc[:, [NAME, CDS]]
    new_data = new_data.drop(columns=[CDS])
    return DataStream(new_data), DataStream(cds_data)
