import unittest
from typing import final, override

from ..errors import Result
from ..history import History, load_history
from .input_dates import input_class_date


@final
class InputClassDateTest(unittest.TestCase):
    history: Result[History]  # pyright: ignore [reportUninitializedInstanceVariable]

    @override
    def setUp(self) -> None:
        self.history = load_history()

    def test_input_class_date(self) -> None:
        history = self.history.unwrap()
        self.assertEqual(
            input_class_date(history),
            ["08/07/2025", "09/07/2025", "14/07/2025", "16/07/2025"],
        )


if __name__ == "__main__":
    _ = unittest.main()
