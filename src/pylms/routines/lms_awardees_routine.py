from ..cache import cache_for_cmd
from ..cli import interact
from ..data import DataStore
from ..data_service import save
from ..history import History, record_merit, save_history
from ..info import print_info, printpass
from ..result_collate import collate_fast_track, collate_merge, collate_merit
from ..result_utils import mail_result


def run_awardees_lms(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Collate Fast Track Awardees",
        "Collate Merit Awardees",
        "Merge Fast Track and Merit Awardees",
        "Email Results to Students",
        "Return to Previous Menu",
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
                result = collate_fast_track(ds)
                if result.is_err():
                    continue

                printpass("Recorded Fast Track Awardees.\n")
            case 2:
                result = collate_merit(ds, history)
                if result.is_err():
                    continue

                printpass("Recorded Merit Awardees.\n")
                result = record_merit(history)
                if result.is_err():
                    continue

            case 3:
                result = collate_merge(ds)
                if result.is_err():
                    continue

                printpass("Merit and Fast Track Awardees merged successfully\n")
            case 4:
                if history.has_collated_merit:
                    result = mail_result(ds)
                    if result.is_err():
                        continue

                    printpass("Email sent successfully\n")
                else:
                    print_info(
                        "Collate Merit Awardees first, before emailing results.\n"
                    )
            case 5:
                break
            case _:
                pass

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
