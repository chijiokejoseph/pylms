import unittest

from .class_nums import parse_class_nums


class TestParseClassNum(unittest.TestCase):
    """

    Each test covers a focused parsing scenario and asserts the expected list
    of integers is returned (via the `Result` wrapper).
    """

    def test_single_int(self) -> None:
        """Parse a single integer string.

        Verifies that a single integer input like "12" produces a one-element
        list [12].

        Returns:
            None
        """
        self.assertEqual(parse_class_nums("12").unwrap(), [12])

    def test_multiple_ints(self) -> None:
        """Parse multiple comma-separated integers.

        Verifies that inputs such as "1, 3, 5" are parsed into [1, 3, 5].

        Returns:
            None
        """
        self.assertEqual(
            parse_class_nums("1, 3, 5").unwrap(),
            [1, 3, 5],
        )

    def test_int_range(self) -> None:
        """Parse integer ranges and individual integers.

        Verifies that ranges like "1 - 6" are expanded and combined with single
        integers (e.g. "1 - 6, 8") to produce the full list in ascending order.

        Returns:
            None
        """
        self.assertEqual(parse_class_nums("1 - 6, 8").unwrap(), [1, 2, 3, 4, 5, 6, 8])

    def test_invalid_input(self) -> None:
        """Handle completely invalid input gracefully.

        An input that cannot be parsed (for example "invalid date") should
        result in an empty list rather than raising an exception.

        Returns:
            None
        """
        self.assertEqual(parse_class_nums("invalid date").unwrap(), [])

    def test_malformed_string(self) -> None:
        """Handle malformed numeric strings.

        Inputs with malformed range syntax or unexpected characters should be
        handled gracefully and yield an empty result list.

        Returns:
            None
        """
        self.assertEqual(parse_class_nums("1 -* 52").unwrap(), [])


if __name__ == "__main__":
    _ = unittest.main()
