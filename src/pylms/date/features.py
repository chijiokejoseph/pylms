from datetime import datetime

from dateutil.parser import parse

from ..constants import DATE_FMT


def det_week_num() -> int:
    """Get current week number.
    
    Returns:
        int: ISO week number of current date.
    """
    today: datetime = datetime.now()
    return today.isocalendar().week


def to_week_num(date_string: str) -> int:
    """Convert date string to ISO week number.
    
    Args:
        date_string (str): Date in DATE_FMT format.
        
    Returns:
        int: ISO week number.
    """
    date_obj: datetime = datetime.strptime(date_string, DATE_FMT)
    return date_obj.isocalendar().week


def to_week_nums(date_string_list: list[str]) -> list[int]:
    """Convert list of date strings to week numbers.
    
    Args:
        date_string_list (list[str]): List of dates in DATE_FMT format.
        
    Returns:
        list[int]: List of ISO week numbers.
    """
    return [to_week_num(date_str) for date_str in date_string_list]


def to_unique_week_nums(date_string_list: list[str]) -> list[int]:
    """Convert date strings to sorted unique week numbers.
    
    Args:
        date_string_list (list[str]): List of dates in DATE_FMT format.
        
    Returns:
        list[int]: Sorted list of unique ISO week numbers.
    """
    # Get unique week numbers and sort them
    week_nums: list[int] = list(set(to_week_nums(date_string_list)))
    week_nums.sort()
    return week_nums


def det_year() -> int:
    """Get current year.
    
    Returns:
        int: Current year.
    """
    return datetime.now().year


def to_day_num(entry: str | datetime) -> int:
    """Convert date to ISO weekday number.
    
    Args:
        entry (str | datetime): Date string or datetime object.
        
    Returns:
        int: ISO weekday number (1=Monday, 7=Sunday).
    """
    if isinstance(entry, str):
        # Parse with day-first format
        date_obj: datetime = parse(entry, dayfirst=True)
    else:
        date_obj = entry
    return date_obj.isoweekday()
