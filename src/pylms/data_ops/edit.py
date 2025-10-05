from typing import Any

import numpy as np
from dateutil.parser import ParserError

from pylms.cli import input_option, input_str, select_student
from pylms.cli.email_input import validate_email
from pylms.constants import (
    COHORT,
    COMMA_DELIM,
    COMPLETION,
    DATA_COLUMNS,
    DATE,
    EMAIL,
    GENDER,
    INTERNSHIP,
    NAME,
    PHONE,
    SERIAL,
    SPACE_DELIM,
    TIME,
)
from pylms.errors import Result, Unit
from pylms.preprocess.clean import re_phone
from pylms.utils import DataStore, date, print_stream


def _preprocess(col_name: str, value: str) -> Any | None:
    """
    Preprocesses and validates the input value for a given column name.

    :param col_name: (str) - The name of the column to preprocess.
    :type col_name: str
    :param value: (str) - The value to preprocess and validate.
    :type value: str
    :return: (Any | None) - The processed value if valid, otherwise None.
    :rtype: Any | None
    """
    value = value.strip()
    # Only process columns defined in DATA_COLUMNS
    if col_name not in DATA_COLUMNS:
        return None

    match True:
        case _ if col_name == NAME:
            # Split name by spaces, require multiple names
            names = value.split(SPACE_DELIM)
            if len(names) == 1:
                print(
                    f"\nInvalid {NAME} specified. {NAME} should contain multiple names separated by spaces."
                )
                return None
            # Join names with comma and title-case
            return COMMA_DELIM.join(names).title()
        case _ if col_name == GENDER:
            # Accept only 'Male' or 'Female'
            value_title = value.title()
            if value_title not in ["Male", "Female"]:
                print(
                    f"\nInvalid {GENDER} specified. {GENDER} should be one of two values: Male | Female."
                )
                return None
            return value_title
        case _ if col_name == EMAIL:
            # Validate email format
            if validate_email(value.lower()):
                return value
            print(
                f"\nInvalid {EMAIL} specified. {EMAIL} should be a valid email address."
            )
            return None
        case _ if col_name == INTERNSHIP:
            # Accept only 'NYSC' or 'SIWES'
            if value.upper() not in ["NYSC", "SIWES"]:
                print(
                    f"\nInvalid {INTERNSHIP} specified. {INTERNSHIP} should be one of two values: NYSC | SIWES."
                )
                return None
            return value.upper()
        case _ if col_name == COMPLETION or col_name == DATE:
            # Parse date string
            try:
                return date.parse(value.lower())
            except ParserError:
                print(
                    f"\nInvalid {col_name} specified. {col_name} is not parseable to a datetime."
                )
                return None
        case _ if col_name == COHORT:
            # Parse cohort as integer
            try:
                return int(value)
            except ValueError:
                print(
                    f"\nInvalid {COHORT} specified. {COHORT} is not parseable to an integer."
                )
                return None
        case _ if col_name in [SERIAL, TIME]:
            # SERIAL and TIME are not editable
            return None
        case _ if col_name == PHONE:
            # Split phone numbers by spaces, require multiple numbers
            return re_phone.match_and_clean(value)
        case _:
            return None


def edit(ds: DataStore) -> Result[Unit]:
    """
    Allows the user to edit records for selected students in the DataStore.
    Prompts for student selection, attribute to edit, and new value.
    Updates the DataStore with the new values and returns it.

    :param ds: (DataStore) - The DataStore containing student records to edit.
    :type ds: DataStore
    :return: (Result[Unit]) - The updated DataStore after editing records.
    :rtype: Result[Unit]
    """
    print("\nPlease select the students whose records you wish to edit")
    serials = select_student(ds)
    data_ref = ds.as_ref()
    for serial in serials:
        # Display current record for the selected student
        print_stream(ds, [serial])
        idx = serial - 1
        # Prepare list of editable columns (exclude SERIAL and TIME)
        mutable_cols = DATA_COLUMNS.copy()
        for col in [SERIAL, TIME]:
            mutable_cols.remove(col)
        proc_value: Any | None = None
        column: str = ""
        # Loop until a valid value is entered
        while proc_value is None:
            result = input_option(mutable_cols, "Attribute to Edit")
            if result.is_err():
                return Result[Unit].err(result.unwrap_err())
            _, column = result.unwrap()
            input_result = input_str(f"Enter the new value for {column}: ", lower_case=False)
            if input_result.is_err():
                return Result[Unit].err(input_result.unwrap_err())
            value = input_result.unwrap()
            proc_value = _preprocess(column, value)
            print()

        # Convert new value to correct dtype
        column_type = data_ref.loc[:, column].dtype.type
        new_value: np.ndarray = np.array(proc_value).astype(column_type)
        # For DATE and COHORT, update entire column; otherwise, update single row
        if column in [DATE, COHORT]:
            data_ref.loc[:, column] = new_value
        else:
            data_ref.loc[idx, column] = new_value
        print()
    return Result[Unit].unit()
