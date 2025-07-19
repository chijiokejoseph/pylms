import unittest

from pylms.cli.utils.int_str_parse import _parse_int_str


# all tests pass
class TestIntStringParse(unittest.TestCase):
    def test_single_int(self) -> None:
        self.assertEqual(_parse_int_str("12"), [12])

    def test_multiple_ints(self) -> None:
        self.assertEqual(
            _parse_int_str("1, 3, 5"),
            [1, 3, 5],
        )
        
    def test_int_range(self) -> None:
        self.assertEqual(
            _parse_int_str("1 - 6, 8"),
            [1, 2, 3, 4, 5, 6, 8]
        )

    def test_invalid_date_format(self) -> None:
        self.assertEqual(_parse_int_str("invalid date"), [])

    def test_empty_string(self) -> None:
        self.assertEqual(_parse_int_str("1 -* 52"), [])


if __name__ == "__main__":
    unittest.main()
