import unittest
from pylms.cli.utils.date_strings_parse import parse_to_dates

# all tests clear
# implicitly verifies all tests for funcs in `date_strings_parse.py and date_strings_verify.py`
class TestDateStrings(unittest.TestCase):
    def test_parse_dates(self) -> None:
        from pylms.utils import date
        data: list[tuple[str, list[str]]] = [
            ("14/07/2025, 15/07/2025", ["14/07/2025", "15/07/2025"]),
            ("12 - 14", ["14/07/2025", "15/07/2025", "16/07/2025"]),
            ("1 - 3, 5", ["17/06/2025", "18/06/2025", "23/06/2025", "25/06/2025"]), 
            ("all", date.retrieve_dates())
        ]
        
        for (response, expected) in data:
            self.assertEqual(expected, parse_to_dates(response))