from typing import Literal

from ..cli import input_option
from ..errors import Result, eprint
from ..history import History, get_available_cds_forms, get_available_update_forms
from ..models import CDSFormInfo, UpdateFormInfo


def str_form(form: CDSFormInfo | UpdateFormInfo) -> str:
    return f"{form.title}\n{' ' * 3}Timestamp: {form.timestamp}, ID: {form.uuid}"


def select_form(
    history: History, kind: Literal["cds", "update"]
) -> Result[CDSFormInfo | UpdateFormInfo]:
    available_forms: list[CDSFormInfo] | list[UpdateFormInfo] = (
        get_available_cds_forms(history)
        if kind == "cds"
        else get_available_update_forms(history)
    )
    forms_list: list[str] = [str_form(form) for form in available_forms]
    title: str = kind.upper() if kind == "cds" else kind.title()
    if len(forms_list) == 0:
        msg: str = f"list of {title} forms is empty"
        eprint(f"{msg}\n")
        return Result.err(msg)
    option_result = input_option(
        forms_list, prompt=f"Select the {title} Form to retrieve its metadata"
    )
    if option_result.is_err():
        return option_result.propagate()
    num, _ = option_result.unwrap()
    idx: int = num - 1
    return Result.ok(available_forms[idx])
