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
    def test_get_held_classes(self) -> None:
        history = load_history().unwrap()
        values = get_held_classes(history, "")
        non_values = get_unheld_classes(history, "")
        print(f"{values = }")
        print(f"{non_values = }")

    def test_get_marked_classes(self) -> None:
        history = load_history().unwrap()
        values = get_marked_classes(history, "")
        non_values = get_unmarked_classes(history, "")
        print(f"{values = }")
        print(f"{non_values = }")


if __name__ == "__main__":
    _ = unittest.main()
