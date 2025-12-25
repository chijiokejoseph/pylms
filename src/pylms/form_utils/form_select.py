from collections.abc import Callable
from typing import Literal, overload

from pylms.info import print_info

from ..cli import input_option
from ..errors import Result, eprint
from ..history import History, get_available_cds_forms, get_available_update_forms
from ..models import CDSFormInfo, UpdateFormInfo


def str_form(form: CDSFormInfo | UpdateFormInfo) -> str:
    return f"{form.title}\n{' ' * 3}Timestamp: {form.timestamp}, ID: {form.uuid}"


def select[T](
    choices: list[T], prompt: str, func: Callable[[T], str] = str
) -> Result[T]:
    menu = [func(choice) for choice in choices]
    result = input_option(menu, prompt)
    if result.is_err():
        return result.propagate()
    num, _ = result.unwrap()
    idx: int = num - 1
    return Result.ok(choices[idx])


@overload
def select_form(history: History, kind: Literal["cds"]) -> Result[CDSFormInfo]:
    pass


@overload
def select_form(history: History, kind: Literal["update"]) -> Result[UpdateFormInfo]:
    pass


def select_form(
    history: History, kind: Literal["cds", "update"]
) -> Result[CDSFormInfo] | Result[UpdateFormInfo]:
    available_forms: list[CDSFormInfo] | list[UpdateFormInfo] = (
        get_available_cds_forms(history)
        if kind == "cds"
        else get_available_update_forms(history)
    )

    cds_forms: list[CDSFormInfo] = []
    update_forms: list[UpdateFormInfo] = []

    for form in available_forms:
        if isinstance(form, CDSFormInfo):
            cds_forms.append(form)
        else:
            update_forms.append(form)

    forms_list: list[str] = [str_form(form) for form in available_forms]
    title: str = kind.upper() if kind == "cds" else kind.title()
    if len(forms_list) == 0:
        msg: str = f"list of {title} forms is empty"
        eprint(f"{msg}\n")
        return Result.err(msg)

    if len(cds_forms) > 0 and len(update_forms) == 0:
        result = select(
            cds_forms, "Select the CDS Form to retrieve its metadata", str_form
        )
        if result.is_err():
            return result.propagate()
        form = result.unwrap()
        return Result.ok(form)
    elif len(cds_forms) == 0 and len(update_forms) > 0:
        result = select(
            update_forms, "Select the Update Form to retrieve its metadata", str_form
        )
        if result.is_err():
            return result.propagate()
        form = result.unwrap()
        return Result.ok(form)
    elif len(cds_forms) == 0 and len(update_forms) == 0:
        msg = "No CDS or Update forms avaiable"
        print_info(msg)
        return Result.err(msg)
    else:
        raise ValueError(
            "Not possible to have both CDS Forms and Update Forms selected at the same time"
        )
