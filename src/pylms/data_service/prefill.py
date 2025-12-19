import pandas as pd

from ..constants import (
    COHORT,
    COMPLETION,
    DATE,
    EMAIL,
    GENDER,
    INTERNSHIP,
    NAME,
    PHONE,
    SERIAL,
    TIME,
    TRAINING,
)
from ..data import DataStore


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
