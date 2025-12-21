"""Data cleaning utilities package.

This package provides focused helpers to normalize and clean tabular data used
throughout the project. Functions address common data hygiene tasks such as
normalizing column names, cleaning email and phone fields, trimming and
standardizing string fields, parsing and normalizing dates and times, removing
or marking missing values, de-duplicating rows, and preparing training-related
fields for downstream processing.

The exported functions are small and composable so they can be used together
in cleaning pipelines applied to pandas DataFrames.

Exports (selected):
- clean_col_names, clean_columns, clean_na, clean_duplicates,
- clean_duplicates_with_cols, clean_str, clean_email, clean_name, clean_phone,
- clean_cohort, clean_date, clean_time, clean_internship, clean_training,
- clean_completion_date, clean_sort, clean_order, normalize
"""

from .clean_col_names import clean_col_names
from .clean_columns import clean_columns
from .clean_completion_date import clean_completion_date
from .clean_duplicates import clean_duplicates, clean_duplicates_with_cols
from .clean_email import clean_email
from .clean_info import (
    clean_cohort,
    clean_date,
)
from .clean_internship import clean_internship
from .clean_na import clean_na
from .clean_name import clean_name
from .clean_order import clean_order
from .clean_phone import clean_phone
from .clean_sort import clean_sort
from .clean_states import normalize
from .clean_str import clean_str
from .clean_time import clean_time
from .clean_training import clean_training

__all__ = [
    "clean_col_names",
    "clean_columns",
    "clean_na",
    "clean_duplicates",
    "clean_duplicates_with_cols",
    "clean_str",
    "clean_email",
    "clean_name",
    "clean_phone",
    "clean_cohort",
    "clean_date",
    "clean_time",
    "clean_internship",
    "clean_training",
    "clean_completion_date",
    "clean_sort",
    "clean_order",
    "normalize",
]
