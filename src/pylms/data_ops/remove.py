from pylms.cli import select_student
from pylms.data_ops.sub import sub
from pylms.utils import DataStore


def remove_students(ds: DataStore) -> None:
    student_serials: list[int] = select_student(ds)
    sub(ds, student_serials)
