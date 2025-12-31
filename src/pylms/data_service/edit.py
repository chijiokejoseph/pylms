from typing import Any

import numpy as np
from dateutil.parser import ParserError, parse

from pylms.info import print_info

from ..cli import input_bool, input_option, input_str, provide_serials
from ..cli_utils import verify_email
from ..constants import (
    COHORT,
    COMMA_DELIM,
    COMPLETION,
    COMPLETION_FMT,
    DATA_COLUMNS,
    DATE,
    DATE_FMT,
    EMAIL,
    GENDER,
    INTERNSHIP,
    NAME,
    PHONE,
    SERIAL,
    SPACE_DELIM,
    TIME,
)
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..re_phone import match_and_clean

type Array[K: np.generic] = np.ndarray[tuple[int, ...], np.dtype[K]]


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
                eprint(
                    f"Invalid {NAME} specified. {NAME} should contain multiple names separated by spaces."
                )
                return None
            # Join names with comma and title-case
            return COMMA_DELIM.join(names).title()

        case _ if col_name == GENDER:
            # Accept only 'Male' or 'Female'
            value = value.title()
            if value not in ["Male", "Female"]:
                eprint(
                    f"Invalid {GENDER} specified. {GENDER} should be one of two values: Male | Female."
                )
                return None
            return value

        case _ if col_name == EMAIL:
            # Validate email format
            if verify_email(value.lower()):
                return value
            eprint(
                f"Invalid {EMAIL} specified. {EMAIL} should be a valid email address."
            )
            return None

        case _ if col_name == INTERNSHIP:
            # Accept only 'NYSC' or 'SIWES'
            if value.upper() not in ["NYSC", "SIWES"]:
                eprint(
                    f"Invalid {INTERNSHIP} specified. {INTERNSHIP} should be one of two values: NYSC | SIWES."
                )
                return None
            return value.upper()

        case _ if col_name == COMPLETION or col_name == DATE:
            # Parse date string
            try:
                date = parse(value.lower())
                if col_name == DATE:
                    return date.strftime(DATE_FMT)

                return date.strftime(COMPLETION_FMT)

            except ParserError:
                eprint(
                    f"Invalid {col_name} specified. {col_name} is not parseable to a datetime."
                )
                return None

        case _ if col_name == COHORT:
            # Parse cohort as integer
            try:
                return int(value)
            except ValueError:
                eprint(
                    f"Invalid {COHORT} specified. {COHORT} is not parseable to an integer."
                )
                return None

        case _ if col_name in [SERIAL, TIME]:
            # SERIAL and TIME are not editable
            return None

        case _ if col_name == PHONE:
            # Split phone numbers by spaces, require multiple numbers
            return match_and_clean(value)

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
    print_info("Please select the students whose records you wish to edit")

    serials = provide_serials(ds)
    if serials.is_err():
        return serials.propagate()

    serials = serials.unwrap()
    data_ref = ds.as_ref()

    for serial in serials:
        idx = serial - 1
        # Prepare list of editable columns (exclude SERIAL and TIME)
        mutable_cols = DATA_COLUMNS.copy()
        for col in [SERIAL, TIME]:
            mutable_cols.remove(col)
        proc_value: Any | None = None
        column: str = ""

        name = data_ref[NAME].astype(str).iloc[idx]
        print_info(f"You are editing the record of {name} with serial {serial}")

        # Loop until a valid value is entered
        while proc_value is None:
            result = input_option(mutable_cols, "Attribute to Edit")
            if result.is_err():
                return result.propagate()
            _, column = result.unwrap()

            old_value = data_ref[column].astype(str).iloc[idx]

            print_info(
                f"Existing Record\nSerial: {serial}\nStudent {name}\n{column}: {old_value}\n"
            )

            result = input_str(f"Enter the new value for {column}: ", lower_case=False)
            if result.is_err():
                return result.propagate()
            value = result.unwrap()
            proc_value = _preprocess(column, value)
            print()

            print_info(
                f"New Record\nSerial: {serial}\nStudent {name}\n{column}: {proc_value}\n"
            )

            choice = input_bool("Confirm this edit: ")
            if choice.is_err():
                continue
            choice = choice.unwrap()

            if choice:
                break

        # Convert new value to correct dtype
        column_type = data_ref.loc[:, column].dtype.type
        new_value: Array[Any] = np.array(proc_value).astype(column_type)
        # For DATE and COHORT, update entire column; otherwise, update single row
        if column in [DATE, COHORT]:
            data_ref.loc[:, column] = new_value
        else:
            data_ref.loc[idx, column] = new_value
        print()
    return Result.unit()
