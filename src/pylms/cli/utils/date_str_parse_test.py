import unittest

from pylms.cli.utils.date_str_parse import _parse_date_str


# all tests pass
class TestDateStringParse(unittest.TestCase):
    def test_single_date(self) -> None:
        self.assertEqual(_parse_date_str("12/11/2023"), ["12/11/2023"])

    def test_multiple_dates(self) -> None:
        self.assertEqual(
            _parse_date_str("12/11/2023, 01/05/2024"),
            ["12/11/2023", "01/05/2024"],
        )

    def test_invalid_date_format(self) -> None:
        self.assertEqual(_parse_date_str("invalid date"), [])

    def test_empty_string(self) -> None:
        self.assertEqual(_parse_date_str(""), [])
        
        
if __name__ == "__main__":
    unittest.main()