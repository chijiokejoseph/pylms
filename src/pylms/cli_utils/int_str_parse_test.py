import unittest

from .int_str_parse import parse_int_str


# all tests pass
class TestIntStringParse(unittest.TestCase):
    """
    Test suite for the _parse_int_str function in src.cli.utils.int_str_parse.

    This class contains unit tests to verify the correct parsing of integer strings
    into lists of integers, including handling of single integers, multiple integers,
    ranges, invalid formats, and empty strings.
    """

    def test_single_int(self) -> None:
        """
        Test parsing a single integer string.

        :return: (None) - returns nothing
        :rtype: None
        """
        # Assert that a single integer string returns a list with that integer
        self.assertEqual(parse_int_str("12").unwrap(), [12])

    def test_multiple_ints(self) -> None:
        """
        Test parsing a string containing multiple comma-separated integers.

        :return: (None) - returns nothing
        :rtype: None
        """
        # Assert that multiple integers separated by commas are parsed into a list of integers
        self.assertEqual(
            parse_int_str("1, 3, 5").unwrap(),
            [1, 3, 5],
        )

    def test_int_range(self) -> None:
        """
        Test parsing a string containing integer ranges and individual integers.

        :return: (None) - returns nothing
        :rtype: None
        """
        # Assert that integer ranges and individual integers are parsed correctly into a list of integers
        self.assertEqual(parse_int_str("1 - 6, 8").unwrap(), [1, 2, 3, 4, 5, 6, 8])

    def test_invalid_date_format(self) -> None:
        """
        Test parsing an invalid integer string.

        :return: (None) - returns nothing
        :rtype: None
        """
        # Assert that an invalid integer string returns an empty list
        self.assertEqual(parse_int_str("invalid date").unwrap(), [])

    def test_empty_string(self) -> None:
        """
        Test parsing an empty or malformed integer string.

        :return: (None) - returns nothing
        :rtype: None
        """
        # Assert that an empty or malformed integer string returns an empty list
        self.assertEqual(parse_int_str("1 -* 52").unwrap(), [])


if __name__ == "__main__":
    _ = unittest.main()
