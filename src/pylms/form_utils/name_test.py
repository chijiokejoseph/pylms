import unittest
from unittest import TestCase

from ..info import print_info
from .name import return_name


class TestName(TestCase):
    """Test cases for form name generation functionality."""
    
    def test_name(self) -> None:
        """Test return_name function with different function types and dates.
        
        Tests form title and name generation for assessment forms (no date)
        and attendance forms (with specific dates).
        """
        cohort = 31
        samples: list[tuple[str, str | None]] = [
            ("Assessment", None),
            ("Excused", "15/12/2025"),
            ("Present", "15/12/2025"),
        ]

        for function, date in samples:
            head = return_name(cohort, function, date)
            form_title, form_name = head.title, head.name
            print_info(f"For function: {function} and date: {date}")
            print_info(f"Title: {form_title}")
            print_info(f"Name: {form_name}")


if __name__ == "__main__":
    _ = unittest.main()
