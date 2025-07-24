"""
This package clean_pipeline is a custom package that encapsulates the cleaning functionalities of the subpackage `clean` of the `utils` package. It encapsulates the cleaning functions contained in the subpackage `clean` and creates a higher level function for formatting two different cases of data input

    - Registration / New Data Input: It cleans data passed in as a `DataStream` object from the registration data for a new cohort and returns a `DataStore` object. This is achieved using the `clean_reg_data` function.

    - Post Registration / Extra Data Input: This package cleans data that is to be added to the registration data from the previous case. It also takes in a `DataStream` object from this extra data and returns a `DataStore` object that is now added to the initial `DataStream` object using the functions from the `data_ops` package

"""

from pylms.preprocess.clean_pipeline.clean_reg_data import clean_reg_data
from pylms.preprocess.clean_pipeline.clean_new_data import clean_new_data

__all__ = [
    "clean_reg_data",
    "clean_new_data",
]
