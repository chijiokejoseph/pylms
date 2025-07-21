from pylms.rollcall.record.input_dates import input_class_date
from pylms.history import History
import unittest


class InputClassDateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.history = History.load()

    def test_input_class_date(self) -> None:
        
        self.assertEqual(
            input_class_date(self.history),
            ["08/07/2025", "09/07/2025", "14/07/2025", "16/07/2025"],
        )


if __name__ == "__main__":
    unittest.main()
