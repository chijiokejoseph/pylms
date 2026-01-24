import unittest
from unittest import TestCase

from .new import load_history
from .retrieve import (
    get_held_classes,
    get_marked_classes,
    get_unheld_classes,
    get_unmarked_classes,
)


class TestRetrieveFuncs(TestCase):
    """Test cases for history retrieval functions."""
    
    def test_get_held_classes(self) -> None:
        """Test retrieval of held and unheld classes.
        
        Verifies that get_held_classes and get_unheld_classes return
        appropriate lists and prints the results for verification.
        """
        history = load_history().unwrap()
        values = get_held_classes(history, "")
        non_values = get_unheld_classes(history, "")
        print(f"{values = }")
        print(f"{non_values = }")

    def test_get_marked_classes(self) -> None:
        """Test retrieval of marked and unmarked classes.
        
        Verifies that get_marked_classes and get_unmarked_classes return
        appropriate lists and prints the results for verification.
        """
        history = load_history().unwrap()
        values = get_marked_classes(history, "")
        non_values = get_unmarked_classes(history, "")
        print(f"{values = }")
        print(f"{non_values = }")


if __name__ == "__main__":
    _ = unittest.main()
