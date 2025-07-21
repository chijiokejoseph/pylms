from pylms.history.history import History
from pylms.constants import HISTORY_PATH
import unittest

class TestHistoryClass(unittest.TestCase):
    def test_history_load(self) -> None:
        """
        Tests that the history can be loaded and saved.

        :return: (None) - This method does not return anything.
        :rtype: None
        """
        history = History.load()
        history.save()
        # get the third class details
        num: int = 2
        third_class_date = history.class_forms[num - 1].date
        print(f"{third_class_date = }")
        self.assertTrue(HISTORY_PATH.exists())
        self.assertEqual(third_class_date, "18/06/2025")
        
if __name__ == "__main__":
    unittest.main()
        