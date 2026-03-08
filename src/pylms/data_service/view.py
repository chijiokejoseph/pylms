from ..data import DataStore, print_stream
from ..errors import Result, Unit
from ..query_data import run_query_data


def view(ds: DataStore) -> Result[Unit]:
    """Display selected students from DataStore.

    Args:
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[Unit]: Success or error message.
    """
    student_serials = run_query_data(ds)
    if student_serials.is_err():
        return student_serials.propagate()

    student_serials = student_serials.unwrap()
    print_stream(ds, student_serials)
    return Result.unit()
