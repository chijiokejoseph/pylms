from ..constants import CDS, NAME
from ..data import DataStream


def extract_cds(
    data_form_stream: DataStream,
) -> tuple[DataStream, DataStream]:
    """Extract CDS information from form data stream.

    Args:
        data_form_stream (DataStream): Stream containing form data with CDS column.

    Returns:
        tuple[DataStream, DataStream]: Tuple of (data without CDS, CDS data only).
    """
    data = data_form_stream.as_ref()
    cds_data = data.select([NAME, CDS])
    new_data = data.drop(CDS)
    return DataStream(new_data), DataStream(cds_data)
