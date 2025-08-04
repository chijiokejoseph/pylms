import unittest

from pylms.cli.utils.date_str_parse import _parse_date_str


# all tests pass
class TestDateStringParse(unittest.TestCase):
    """
    Test suite for the _parse_date_str function in pylms.cli.utils.date_str_parse.

    This class contains unit tests to verify the correct parsing of date strings
    into lists of date strings, including handling of single dates, multiple dates,
    invalid formats, and empty strings.
    """

    def test_single_date(self) -> None:
        """
        Test parsing a single date string.

        :return: (None) - returns nothing
        :rtype: None
        """
        # Assert that a single date string returns a list with that date
        self.assertEqual(_parse_date_str("12/11/2023"), ["12/11/2023"])

    def test_multiple_dates(self) -> None:
        """
        Test parsing a string containing multiple comma-separated dates.

        :return: (None) - returns nothing
        :rtype: None
        """
        # Assert that multiple dates separated by commas are parsed into a list of dates
        self.assertEqual(
            _parse_date_str("12/11/2023, 01/05/2024"),
            ["12/11/2023", "01/05/2024"],
        )

    def test_invalid_date_format(self) -> None:
        """
        Test parsing an invalid date string.

        :return: (None) - returns nothing
        :rtype: None
        """
        # Assert that an invalid date string returns an empty list
        self.assertEqual(_parse_date_str("invalid date"), [])

    def test_empty_string(self) -> None:
        """
        Test parsing an empty string.

        :return: (None) - returns nothing
        :rtype: None
        """
        # Assert that an empty string returns an empty list
        self.assertEqual(_parse_date_str(""), [])


if __name__ == "__main__":
    unittest.main()
