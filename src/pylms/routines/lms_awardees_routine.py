from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.data_ops import save
from pylms.errors import eprint
from pylms.history import History
from pylms.info import println, printpass
from pylms.lms import collate_fast_track, collate_merge, collate_merit, send_result
from pylms.utils import DataStore


def run_awardees_lms(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Collate Fast Track Awardees",
        "Collate Merit Awardees",
        "Merge Fast Track and Merit Awardees",
        "Email Results to Students",
        "Return to Previous Menu",
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
                collate_fast_track(ds)
                printpass("Recorded Fast Track Awardees.\n")
            case 2:
                result = collate_merit(ds, history)
                if result.is_err():
                    continue
                printpass("Recorded Merit Awardees.\n")
                history.record_merit()
            case 3:
                collate_merge(ds)
                printpass("Merit and Fast Track Awardees merged successfully\n")
            case 4:
                if history.has_collated_merit:
                    send_result(ds)
                    printpass("Email sent successfully\n")
                else:
                    println("Collate Merit Awardees first, before emailing results.\n")
            case 5:
                break
            case _:
                pass

        save(ds)
        history.save()

    return None
