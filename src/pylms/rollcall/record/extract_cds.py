from pylms.utils import DataStream
from pylms.constants import CDS, NAME
import pandas as pd


def extract_cds(
    data_form_stream: DataStream[pd.DataFrame],
) -> tuple[DataStream[pd.DataFrame], DataStream[pd.DataFrame]]:
    data: pd.DataFrame = data_form_stream()
    new_data = data.copy()
    cds_data: pd.DataFrame = new_data.loc[:, [NAME, CDS]]
    new_data = new_data.drop(columns=[CDS])
    return DataStream(new_data), DataStream(cds_data)
