from ..cache import cache_for_cmd
from ..cli import interact
from ..data import DataStore
from ..data_service import save
from ..form_request import request_assessment_form
from ..history import History, get_num_groups, save_history
from ..info import print_info, printpass
from ..lms import (
    group,
    select_leaders,
)
from ..result_utils import prepare_grading
from .lms_awardees_routine import run_awardees_lms
from .lms_collate_routine import run_collate_lms
from .lms_result_routine import run_result_lms


def run_lms(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Group Students",
        "Request Assessment Form Template",
        "Collate Student Metrics",
        "Manage Results",
        "Manage Awardees",
        "Return to Main Menu",
    ]

    while True:
        selection = interact(menu)
        if selection.is_err():
            continue

        selection = selection.unwrap()

        cmd: str = menu[selection - 1]

        if selection < len(menu):
            result = cache_for_cmd(cmd)
            if result.is_err():
                continue

        match selection:
            case 1:
                result = group(ds, history)
                if result.is_err():
                    continue

                printpass("Students have been grouped successfully\n")

                if history.has_group:
                    num_groups: int = get_num_groups(history)

                    result = prepare_grading(num_groups)
                    if result.is_err():
                        continue

                    printpass("Grading sheets generated successfully")

                    result = select_leaders(ds, history)
                    if result.is_err():
                        continue

                    printpass("Leaders have been selected successfully\n")
            case 2:
                request_assessment_form(ds)
            case 3:
                run_collate_lms(ds, history)
            case 4:
                run_result_lms(ds, history)
            case 5:
                run_awardees_lms(ds, history)
            case _:
                break

        result = save(ds)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

        result = save_history(history)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

    return None
