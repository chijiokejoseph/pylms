import unittest
from typing import final, override

from ..errors import Result
from ..history import History, load_history
from .input_dates import input_class_date


@final
class InputClassDateTest(unittest.TestCase):
    """Unit tests for input_class_date function.
    
    Tests the functionality of selecting class dates for attendance marking.
    """
    history: Result[History]  # pyright: ignore [reportUninitializedInstanceVariable]

    @override
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.history = load_history()

    def test_input_class_date(self) -> None:
        """Test that input_class_date returns expected date list."""
        history = self.history.unwrap()
        self.assertEqual(
            input_class_date(history),
            ["08/07/2025", "09/07/2025", "14/07/2025", "16/07/2025"],
        )


if __name__ == "__main__":
    _ = unittest.main()
