from ..clean import (
    clean_cohort,
    clean_col_names,
    clean_completion_date,
    clean_date,
    clean_duplicates,
    clean_email,
    clean_internship,
    clean_na,
    clean_name,
    clean_order,
    clean_phone,
    clean_sort,
    clean_time,
    clean_training,
)
from ..cli import input_path
from ..data import DataStore, DataStream, read
from ..errors import Result


def clean_reg(data_stream: DataStream) -> Result[DataStore]:
    """Clean registration data through comprehensive preprocessing pipeline.

    Performs extensive data cleaning operations including column renaming,
    duplicate removal, NA handling, string formatting, email/name/phone cleaning,
    cohort/date standardization, and final sorting and ordering.

    Args:
        data_stream (DataStream): Stream containing raw registration data.

    Returns:
        Result[DataStore]: Success with cleaned DataStore or error.
    """
    data = data_stream.as_ref()
    data = clean_col_names(data)

    result = clean_na(data)
    if result.is_err():
        return result.propagate()

    data = result.unwrap()

    data = clean_email(data)
    data = clean_name(data)
    result = clean_phone(data)
    if result.is_err():
        return result.propagate()

    data = result.unwrap()
    
    result = clean_cohort(data)
    if result.is_err():
        return result.propagate()

    data = result.unwrap()

    result = clean_date(data)
    if result.is_err():
        return result.propagate()

    data = result.unwrap()

    data = clean_time(data)
    data = clean_internship(data)
    data = clean_training(data)

    result = clean_completion_date(data)
    if result.is_err():
        return result.propagate()

    data = result.unwrap()

    data = clean_duplicates(data)
    data = clean_sort(data)

    result = clean_order(data)
    if result.is_err():
        return result.propagate()

    data = result.unwrap()

    return Result.ok(DataStore(data))


def clean_reg_data() -> Result[DataStore]:
    """Prompt user for registration spreadsheet path and clean the data.

    Prompts user to enter path to registration Excel file, reads it,
    and processes it through the complete data cleaning pipeline.

    Returns:
        Result[DataStore]: Success with cleaned registration DataStore or error.
    """
    msg = """Enter the absolute path to the new cohort spreadsheet for the students.
Enter the path:  """

    result = input_path(msg)
    if result.is_err():
        return result.propagate()
    register_path = result.unwrap()
    dataframe = read(register_path, True)
    if dataframe.is_err():
        return dataframe.propagate()
    dataframe = dataframe.unwrap()
    register_ds = DataStream(dataframe)
    return clean_reg(register_ds)
