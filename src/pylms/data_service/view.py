from ..cli import provide_serials
from ..data import DataStore, print_stream
from ..errors import Result, Unit


def view(ds: DataStore) -> Result[Unit]:
    student_serials = provide_serials(ds)
    if student_serials.is_err():
        return student_serials.propagate()

    student_serials = student_serials.unwrap()
    print_stream(ds, student_serials)
    return Result.unit()
