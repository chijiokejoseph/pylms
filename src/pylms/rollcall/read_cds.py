from ..constants import CDS, NAME
from ..data import DataStream


def extract_cds(
    data_form_stream: DataStream,
) -> tuple[DataStream, DataStream]:
    data: pl.DataFrame = data_form_stream.as_clone()
    cds_data: pl.DataFrame = data.loc[:, [NAME, CDS]]
    new_data = data.drop(columns=[CDS])
    return DataStream(new_data), DataStream(cds_data)
