from pylms.utils import DataStore
from pylms.constants import (
    SERIAL,
    TIME,
    NAME,
    GENDER,
    COHORT,
    PHONE,
    EMAIL,
    DATE,
    INTERNSHIP,
    COMPLETION,
    TRAINING,
)

import pandas as pd


def prefill_ds() -> DataStore:
    dummy_data: pd.DataFrame = pd.DataFrame(
        data={
            SERIAL: [0, 0],
            TIME: ["00:00", "00:00"],
            NAME: ["", ""],
            GENDER: ["", ""],
            COHORT: [0, 0],
            PHONE: ["", ""],
            EMAIL: ["", ""],
            DATE: ["", ""],
            INTERNSHIP: ["", ""],
            COMPLETION: ["", ""],
            TRAINING: ["", ""],
        }
    )
    ds: DataStore = DataStore(dummy_data)
    ds.prefilled = True
    return ds
