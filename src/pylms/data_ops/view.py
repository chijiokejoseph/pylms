from pylms.cli import select_student
from pylms.utils import DataStore, print_stream


def view(ds: DataStore) -> None:
    student_serials = select_student(ds)
    print_stream(ds, student_serials)
