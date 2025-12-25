from pathlib import Path

from ..cli import provide_serials
from ..data import DataStore, DataStream, print_stream, read
from ..errors import Result, Unit, eprint
from ..paths import get_paths_excel
from .val import val_result_data


def view_result(ds: DataStore) -> Result[Unit]:
    result_path: Path = get_paths_excel()["Result"]
    if not result_path.exists():
        msg = "Results has not been generated yet. Please collate results before running this operation"
        eprint(msg)
        return Result.err(msg)

    result_data = read(result_path)

    if result_data.is_err():
        return result_data.propagate()
    result_data = result_data.unwrap()

    result_stream = DataStream(result_data, val_result_data)
    serials = provide_serials(ds)
    if serials.is_err():
        return serials.propagate()

    serials = serials.unwrap()
    print_stream(result_stream, serials)
    return Result.unit()
