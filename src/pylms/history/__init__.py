"""This module provides the History class for managing class history.
It includes methods for adding held and marked classes and updating class dates."""

from .classes import extend_weeks, replan_weeks, set_class_days, sync_classes
from .dates import retrieve_dates
from .dates_with_history import all_dates
from .groups import get_num_groups, set_group
from .history import History
from .interlude import Interlude
from .interlude_funcs import add_interlude
from .lms_records import (
    record_assessment,
    record_attendance,
    record_merit,
    record_project,
    record_result,
)
from .new import load_history
from .num_cohort import set_cohort
from .retrieve import (
    get_available_cds_forms,
    get_available_class_forms,
    get_available_update_forms,
    get_classes,
    get_held_classes,
    get_marked_classes,
    get_unheld_classes,
    get_unmarked_classes,
    get_unrecorded_classes,
    match_date_index,
    match_info_by_date,
)
from .save import save_history
from .update import (
    add_cds_form,
    add_class_form,
    add_held_class,
    add_marked_class,
    add_prop_class,
    add_recorded_cds_form,
    add_recorded_class_form,
    add_recorded_update_form,
    add_update_form,
)

__all__ = [
    "History",
    "Interlude",
    "add_cds_form",
    "add_class_form",
    "add_held_class",
    "add_marked_class",
    "add_prop_class",
    "add_recorded_cds_form",
    "add_recorded_class_form",
    "add_recorded_update_form",
    "add_update_form",
    "add_interlude",
    "all_dates",
    "extend_weeks",
    "replan_weeks",
    "set_class_days",
    "sync_classes",
    "get_num_groups",
    "set_group",
    "record_attendance",
    "record_assessment",
    "record_project",
    "record_merit",
    "record_result",
    "load_history",
    "set_cohort",
    "get_available_cds_forms",
    "get_available_class_forms",
    "get_available_update_forms",
    "get_classes",
    "get_held_classes",
    "get_marked_classes",
    "get_unheld_classes",
    "get_unmarked_classes",
    "get_unrecorded_classes",
    "match_date_index",
    "match_info_by_date",
    "save_history",
    "retrieve_dates",
]
