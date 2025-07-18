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
    SERIAL,
    SPACE_DELIM,
    TIME,
)
from pylms.utils import DataStore, date, print_stream


def _preprocess(col_name: str, value: str) -> Any | None:
    value = value.strip()
    if col_name not in DATA_COLUMNS:
        return None

    match True:
        case _ if col_name == NAME:
            names = value.split(SPACE_DELIM)
            if len(names) == 1:
                print(
                    f"\nInvalid {NAME} specified. {NAME} should contain multiple names separated by spaces."
                )
                return None
            return COMMA_DELIM.join(names).title()
        case _ if col_name == GENDER:
            value_title = value.title()
            if value_title not in ["Male", "Female"]:
                print(
                    f"\nInvalid {GENDER} specified. {GENDER} should be one of two values: Male | Female."
                )
                return None
            return value_title
        case _ if col_name == EMAIL:
            if validate_email(value.lower()):
                return value
            print(
                f"\nInvalid {EMAIL} specified. {EMAIL} should be a valid email address."
            )
            return None
        case _ if col_name == INTERNSHIP:
            if value.upper() not in ["NYSC", "SIWES"]:
                print(
                    f"\nInvalid {INTERNSHIP} specified. {INTERNSHIP} should be one of two values: NYSC | SIWES."
                )
                return None
            return value.upper()
        case _ if col_name == COMPLETION or col_name == DATE:
            try:
                return date.parse(value.lower())
            except ParserError:
                print(
                    f"\nInvalid {col_name} specified. {col_name} is not parseable to a datetime."
                )
                return None
        case _ if col_name == COHORT:
            try:
                return int(value)
            except ValueError:
                print(
                    f"\nInvalid {COHORT} specified. {COHORT} is not parseable to an integer."
                )
                return None
        case _ if col_name in [SERIAL, TIME]:
            return None
        case _:
            return None


def edit(ds: DataStore) -> DataStore:
    print("\nPlease select the students whose records you wish to edit")
    serials = select_student(ds)
    data = ds()
    for serial in serials:
        print_stream(ds, [serial])
        idx = serial - 1
        mutable_cols = DATA_COLUMNS.copy()
        for col in [SERIAL, TIME]:
            mutable_cols.remove(col)
        proc_value: Any | None = None
        column: str = ""
        while proc_value is None:
            _, column = input_option(mutable_cols, "Attribute to Edit")
            value = input_str(f"Enter the new value for {column}: ", lower_case=False)
            proc_value = _preprocess(column, value)
            print()

        column_type = data.loc[:, column].dtype.type
        new_value: np.ndarray = np.array(proc_value).astype(column_type)
        if column in [DATE, COHORT]:
            data.loc[:, column] = new_value
        else:
            data.loc[idx, column] = new_value
        print()
    ds.data = data
    return ds
