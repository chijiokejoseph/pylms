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
- query_emails: Query-based email input with automatic type detection.
- interactive_email_input: Interactive menu-based email input.
- provide_serials: Function to provide student serial numbers in various formats.
- select_class_date: Function to select class dates.
- input_dates: Function to get validated date input.
- print_date_menu: Function to print simple date menu.
- display_dates: Function to display date menu with class numbers.
- select_student: Function to select students.
"""

from .custom_inputs import (
    input_num,
    input_str,
)
from .dates_input import input_dates
from .dates_print import print_date_menu
from .email_input import input_email
from .emails_input import provide_emails
from .emails_inputs import input_emails
from .emails_query import query_emails
from .input_with_quit import input_fn
from .interact import interact
from .menu_input import input_menu
from .option_input import input_bool, input_option
from .path_input import input_path, test_path_in

__all__ = [
    "interact",
    "input_num",
    "input_option",
    "input_bool",
    "input_path",
    "test_path_in",
    "input_str",
    "input_fn",
    "input_email",
    "input_menu",
    "input_dates",
    "print_date_menu",
    "provide_emails",
    "query_emails",
    "input_emails",
]
