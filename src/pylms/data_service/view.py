from ..cli import select_student
from ..data import DataStore, print_stream
from ..errors import Result, Unit


def view(ds: DataStore) -> Result[Unit]:
    student_serials = select_student(ds)
    if student_serials.is_err():
        return student_serials.propagate()

    student_serials = student_serials.unwrap()
    print_stream(ds, student_serials)
    return Result.unit()
