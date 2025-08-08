from pylms.models.form_info import CDSFormInfo, UpdateFormInfo
from pylms.history import History
from pylms.cli import input_option
from pylms.errors import Result
from typing import Literal


def str_form(form: CDSFormInfo | UpdateFormInfo) -> str:
    return f"{form.title}\n{' ' * 3}Timestamp: {form.timestamp}, ID: {form.uuid}"


def select_form(
    history: History, kind: Literal["cds", "update"]
) -> Result[CDSFormInfo | UpdateFormInfo]:
    available_forms: list[CDSFormInfo] | list[UpdateFormInfo] = (
        history.get_available_cds_forms()
        if kind == "cds"
        else history.get_available_update_forms()
    )
    forms_list: list[str] = [str_form(form) for form in available_forms]
    title: str = kind.upper() if kind == "cds" else kind.title()
    if len(forms_list) == 0:
        return Result[CDSFormInfo | UpdateFormInfo].err(ValueError(f"list of {title} forms is empty"))
    num, _ = input_option(
        forms_list, prompt=f"Select the {title} Form to retrieve its metadata"
    )
    idx: int = num - 1
    return Result[CDSFormInfo | UpdateFormInfo].ok(available_forms[idx])
