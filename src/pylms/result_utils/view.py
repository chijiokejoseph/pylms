from ..config import Config
from ..data import DataStore, DataStream, print_stream, read
from ..errors import Result, Unit, eprint
from ..paths import get_paths_excel
from ..query_data import run_query_data
from .val import val_result_data


def view_result(config: Config, ds: DataStore) -> Result[Unit]:
    """View student results from generated result file.

    Reads result data from Excel file and displays selected students' results.

    Args:
        ds (DataStore): DataStore for student serial selection.

    Returns:
        Result[Unit]: Success or error with message.
    """
    result_path = get_paths_excel(config)["Result"]
    if not result_path.exists():
        msg = "Results has not been generated yet. Please collate results before running this operation"
        eprint(msg)
        return Result.err(msg)

    results = read(result_path)

    if results.is_err():
        return results.propagate()
    results = results.unwrap()

    results_stream = DataStream.new(results, val_result_data)
    if results_stream.is_err():
        return results_stream.propagate()

    results_stream = results_stream.unwrap()

    serials = run_query_data(ds)
    if serials.is_err():
        return serials.propagate()

    serials = serials.unwrap()
    print_stream(results_stream, serials)
    return Result.unit()
