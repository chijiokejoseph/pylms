import unittest
from pylms.cli.utils.date_strings_parse import parse_to_dates


# all tests clear
# implicitly verifies all tests for funcs in `date_strings_parse.py and date_strings_verify.py`
class TestDateStrings(unittest.TestCase):
    """
    Test suite for the parse_to_dates function in pylms.cli.utils.date_strings_parse.

    This class contains unit tests to verify the correct parsing of various date string
    formats into lists of date strings, including ranges, multiple dates, and special keywords.
    """

    def test_parse_dates(self) -> None:
        """
        Test parsing various date string formats into lists of dates.

        :return: (None) - returns nothing
        :rtype: None
        """
        from pylms.utils import date

        # Test data: tuples of input string and expected list of date strings
        data: list[tuple[str, list[str]]] = [
            ("14/07/2025, 15/07/2025", ["14/07/2025", "15/07/2025"]),
            ("12 - 14", ["14/07/2025", "15/07/2025", "16/07/2025"]),
            ("1 - 3, 5", ["17/06/2025", "18/06/2025", "23/06/2025", "25/06/2025"]),
            ("all", date.retrieve_dates())
        ]

        # Assert that parse_to_dates returns expected lists for each input string
        for (response, expected) in data:
            self.assertEqual(expected, parse_to_dates(response))
            
            
            