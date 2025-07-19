from pylms.forms.utils.service import create_form, setup_form, share_form
from pylms.models.form_info import CDSFormInfo, UpdateFormInfo
from pylms.state import History
from pylms.cli import input_option
from typing import Literal


def str_form(form: CDSFormInfo | UpdateFormInfo) -> str:
    return f"{form.title}\n{' ' * 3}Timestamp: {form.timestamp}, ID: {form.uuid}"


def select_form(
    history: History, kind: Literal["cds", "update"]
) -> CDSFormInfo | UpdateFormInfo:
    available_forms = (
        history.get_available_cds_forms()
        if kind == "cds"
        else history.get_available_update_forms()
    )
    cds_forms_list: list[str] = [str_form(form) for form in available_forms]
    num, _ = input_option(
        cds_forms_list, prompt="Select the CDS Form to retrieve data from"
    )
    idx = num - 1
    return available_forms[idx]


__all__: list[str] = [
    "create_form",
    "setup_form",
    "share_form",
    "select_form",
]
