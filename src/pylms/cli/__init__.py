

"""
CLI package for pylms project.

This package contains modules and functions related to command-line interface
interactions, including input handling, user interaction, onboarding requests,
and selection utilities.

Exports:
- interact: Main interaction function.
- input_num: Function to input numbers.
- input_str: Function to input strings.
- input_email: Function to input email addresses.
- confirm_onboard_req: Function to confirm onboarding requests.
- input_option: Function to input options.
- input_path, test_path_in: Functions to input and test paths.
- input_record: Function to input records.
- provide_emails: Function to provide email addresses in various formats.
- select_class_date: Function to select class dates.
- select_student: Function to select students.
"""

from pylms.cli.custom_inputs import (
    input_num,
    input_str,
)
from pylms.cli.email_input import input_email
from pylms.cli.interact import interact
from pylms.cli.onboard_req import confirm_onboard_req
from pylms.cli.option_input import input_option
from pylms.cli.path_input import input_path, test_path_in
from pylms.cli.record_input import input_record
from pylms.cli.select_class_date import select_class_date
from pylms.cli.select_student import select_student
from pylms.cli.emails_input import provide_emails

__all__ = [
    "interact",
    "input_num",
    "input_record",
    "input_option",
    "input_path",
    "test_path_in",
    "input_str",
    "confirm_onboard_req",
    "input_email",
    "select_class_date",
    "select_student",
    "provide_emails",
]
