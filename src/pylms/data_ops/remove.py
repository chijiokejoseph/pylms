from pylms.cli import select_student
from pylms.data_ops.sub import sub
from pylms.utils import DataStore


def remove_students(ds: DataStore) -> DataStore:
    student_serials: list[int] = select_student(ds)
    return sub(ds, student_serials)
