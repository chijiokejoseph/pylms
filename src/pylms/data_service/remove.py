from ..cli import provide_serials
from ..data import DataStore
from ..errors import Result, Unit
from .sub import sub


def remove_students(ds: DataStore) -> Result[Unit]:
    """Remove selected students from DataStore.
    
    Args:
        ds (DataStore): DataStore to remove students from.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    student_serials = provide_serials(ds)
    if student_serials.is_err():
        return student_serials.propagate()

    student_serials = student_serials.unwrap()

    return sub(ds, student_serials)
    
