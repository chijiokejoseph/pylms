from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.data_ops import save
from pylms.errors import eprint
from pylms.forms import request_assessment_form
from pylms.history import History
from pylms.info import printpass
from pylms.lms import (
    group,
    prepare_grading,
    select_leaders,
)
from pylms.routines.lms_awardees_routine import run_awardees_lms
from pylms.routines.lms_collate_routine import run_collate_lms
from pylms.routines.lms_result_routine import run_result_lms
from pylms.utils import DataStore


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
        selection_result = interact(menu)
        if selection_result.is_err():
            eprint(f"Error retrieving selection: {selection_result.unwrap_err()}")
            continue
        selection: int = selection_result.unwrap()
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match selection:
            case 1:
                group(ds, history)
                printpass("Students have been grouped successfully\n")
                if history.has_group():
                    num_groups: int = history.get_num_groups()
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

        save(ds)
        history.save()

    return None
