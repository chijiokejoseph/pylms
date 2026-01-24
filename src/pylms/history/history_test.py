import unittest

from ..constants import HISTORY_PATH
from .new import load_history
from .save import save_history


class TestHistoryClass(unittest.TestCase):
    """Test cases for history loading and saving functionality."""
    
    def test_history_load(self) -> None:
        """Test that history can be loaded and saved successfully.
        
        Verifies that history file exists after save operation and checks
        that specific class form data is correctly loaded.
        """
        history = load_history().unwrap()
        _ = save_history(history).unwrap()
        # Get the third class details
        num: int = 2
        third_class_date = history.class_forms[num - 1].date
        print(f"{third_class_date = }")
        self.assertTrue(HISTORY_PATH.exists())
        self.assertEqual(third_class_date, "18/06/2025")


if __name__ == "__main__":
    _ = unittest.main()
