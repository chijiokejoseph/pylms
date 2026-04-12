"""This module provides the History class for managing class history.
It includes methods for adding held and marked classes and updating class dates."""

from .classes import extend_weeks, replan_weeks, set_class_days, sync_classes
from .dates_with_history import all_dates
from .get_props import (
    get_available_cds_forms,
    get_available_class_forms,
    get_available_update_forms,
    get_class_info,
    get_classes,
    get_date_index,
    get_held_classes,
    get_marked_classes,
    get_manual_classes,
    get_unheld_classes,
    get_unmarked_classes,
    get_unrecorded_classes,
)
from .groups import get_num_groups, set_group
from .history import History
from .interlude_input import new_interlude
from .interlude import Interlude
from .interlude_add import add_interlude
from .lms_records import (
    record_assessment,
    record_attendance,
    record_merit,
    record_project,
    record_result,
)
from .match_classes import match_classes
from .new import init_history, load_history
from .num_cohort import set_cohort
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
    "init_history",
    "load_history",
    "set_cohort",
    "get_available_cds_forms",
    "get_available_class_forms",
    "get_available_update_forms",
    "get_classes",
    "get_held_classes",
    "get_manual_classes",
    "get_marked_classes",
    "get_unheld_classes",
    "get_unmarked_classes",
    "get_unrecorded_classes",
    "get_date_index",
    "get_class_info",
    "new_interlude",
    "match_classes",
    "save_history",
]
