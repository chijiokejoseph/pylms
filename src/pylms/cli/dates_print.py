"""Print function for date menus."""

from ..numutil import max_content_width, max_index_width


def print_date_menu(dates: list[str]) -> None:
    """Print numbered date menu.
    
    Args:
        dates (list[str]): List of dates to display.
    """
    num_width = max_index_width(dates)
    max_width = max_content_width(dates)
    
    for idx, date in enumerate(dates, start=1):
        print(f"{idx:<{num_width}} . {date:{max_width}}")
