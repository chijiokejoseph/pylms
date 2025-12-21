"""
CLI package for src project.

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
- provide_serials: Function to provide student serial numbers in various formats.
- select_class_date: Function to select class dates.
- select_student: Function to select students.
"""

from .custom_inputs import (
    input_num,
    input_str,
)
from .email_input import input_email
from .emails_input import provide_emails
from .input_to_config import input_course_name, input_dir
from .input_with_quit import input_fn
from .interact import interact
from .option_input import input_bool, input_option
from .path_input import input_path, test_path_in
from .select_class_date import select_class_date
from .select_student import select_student
from .serials_input import provide_serials

__all__ = [
    "interact",
    "input_course_name",
    "input_dir",
    "input_num",
    "input_option",
    "input_bool",
    "input_path",
    "test_path_in",
    "input_str",
    "input_fn",
    "input_email",
    "select_class_date",
    "select_student",
    "provide_emails",
    "provide_serials",
]
