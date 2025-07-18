from pylms.cli import select_class_date


def input_date_for_edit() -> list[str]:
    msg: str = "Manual Attendance Marking initiated. \nPlease enter the date(s) for which attendance should be marked if available"
    return select_class_date(msg)
