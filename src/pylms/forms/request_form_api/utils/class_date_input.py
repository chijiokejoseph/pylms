from pylms.cli.select_class_date import select_class_date


def input_class_date() -> list[str]:
    msg: str = "Attendance Form generation initiated. \nPlease enter the date(s) for which the form should be generated."
    return select_class_date(msg)
