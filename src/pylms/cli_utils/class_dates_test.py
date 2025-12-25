"""Unit tests for date string parsing helpers in ``cli_utils``.

This module exercises ``parse_date_str`` from :mod:`pylms.cli_utils.date_str_parse`.
The tests verify correct behavior for single-date input, multiple comma-
separated dates, invalid formats, and empty input. These tests are designed
to be simple, deterministic unit tests that validate the parsing logic.
"""

import unittest

from .class_dates import parse_class_dates


class TestDateStringParse(unittest.TestCase):
    """Unit tests for :func:`pylms.cli_utils.date_str_parse.parse_date_str`.

    The test methods below each cover a focused parsing scenario and assert the
    expected list of date strings is returned.
    """

    def test_single_date(self) -> None:
        """Parse a single date string.

        Verifies that a single date in DD/MM/YYYY format is returned as a
        one-element list.

        Returns:
            None
        """
        self.assertEqual(parse_class_dates("12/11/2023"), ["12/11/2023"])

    def test_multiple_dates(self) -> None:
        """Parse multiple comma-separated date strings.

        Verifies that two dates separated by a comma (with optional whitespace)
        are returned in the same order as a list.

        Returns:
            None
        """
        self.assertEqual(
            parse_class_dates("12/11/2023, 01/05/2024"),
            ["12/11/2023", "01/05/2024"],
        )

    def test_invalid_date_format(self) -> None:
        """Handle invalid date format.

        Ensures that a non-date input yields an empty list rather than raising
        an exception.

        Returns:
            None
        """
        self.assertEqual(parse_class_dates("invalid date"), [])

    def test_empty_string(self) -> None:
        """Handle empty input.

        An empty input string should produce an empty list.

        Returns:
            None
        """
        self.assertEqual(parse_class_dates(""), [])


if __name__ == "__main__":
    _ = unittest.main()
