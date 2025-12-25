"""Unit tests for date string parsing helpers in ``cli_utils``.

This module exercises :func:`pylms.cli_utils.date_strings_parse.parse_to_dates`.
The tests verify correct behavior for range expressions, comma-separated lists,
and the special keyword handling (for example, ``all``). Each test asserts the
expected list of date strings is returned for representative inputs.
"""

import unittest

from ..history import retrieve_dates
from .class_parser import parse_classes


class TestDateStrings(unittest.TestCase):
    """Unit tests for :func:`pylms.cli_utils.date_strings_parse.parse_to_dates`.

    The test methods cover common input forms and assert the parser returns the
    expected list of date strings in each case.
    """

    def test_parse_dates(self) -> None:
        """Verify parsing of ranges, comma-separated dates, and the 'all' keyword.

        Iterates over a set of (input, expected) pairs and asserts that
        `parse_to_dates` produces the expected output for each input.
        """
        data: list[tuple[str, list[str]]] = [
            ("14/07/2025, 15/07/2025", ["14/07/2025", "15/07/2025"]),
            ("12 - 14", ["14/07/2025", "15/07/2025", "16/07/2025"]),
            ("1 - 3, 5", ["17/06/2025", "18/06/2025", "23/06/2025", "25/06/2025"]),
            ("all", retrieve_dates("").unwrap()),
        ]

        for response, expected in data:
            self.assertEqual(expected, parse_classes(response))
