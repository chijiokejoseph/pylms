"""Unit tests for CLI numeric input utilities.

This module contains a small integration-style test that demonstrates usage of
the `input_num` helper used to obtain integer input from a user. The test uses
the project's `Result` error-handling abstraction and prints informational
output via the `print_info` helper.

Note:
- Because `input_num` may prompt for interactive input, this test is intended
  for manual runs or CI environments that can provide input, not as a purely
  automated, non-interactive unit test.
"""

from unittest import TestCase

from ..errors import Result, eprint
from ..info import print_info
from .custom_inputs import input_num


class TestInputs(TestCase):
    """Tests for CLI input helpers.

    These tests exercise interactive input helpers. Each test method documents
    the expected behavior when `input_num` returns either an error `Result` or
    a successful parsed integer value.
    """

    def test_input_num(self) -> None:
        """Exercise `input_num` to read an integer value.

        The test prompts for an integer (minimum 1) using `input_num`. It
        handles the `Result` returned: if the call returns an error the error
        message is printed via `eprint` and the test returns early. On success
        the parsed age is printed via `print_info`.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        value: Result[int] = input_num(
            "Enter your age: ",
            1,
        )
        if value.is_err():
            eprint(f"{value.unwrap_err()}")
            return
        age = value.unwrap()
        print_info(f"Your age is {age}")
