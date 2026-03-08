import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from ..constants import DATE_FMT
from .classes import sync_classes
from .get_props import (
    get_held_classes,
    get_marked_classes,
    get_unheld_classes,
    get_unmarked_classes,
)
from .test_fixtures import create_test_history, load_test_history, save_test_history


class TestRetrieveFuncs(TestCase):
    """Test cases for history retrieval functions."""

    def test_get_held_classes(self) -> None:
        """Test retrieval of held and unheld classes."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        
        # Mark specific classes as held
        history.held_classes = [history.dates[0], history.dates[2], history.dates[5]]
        expected_held = [d.strftime(DATE_FMT) for d in history.held_classes]
        expected_unheld = [d.strftime(DATE_FMT) for d in history.dates if d not in history.held_classes]

        held = get_held_classes(history, "")
        unheld = get_unheld_classes(history, "")

        self.assertEqual(held, expected_held)
        self.assertEqual(unheld, expected_unheld)

    def test_get_marked_classes(self) -> None:
        """Test retrieval of marked and unmarked classes."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        
        # Mark classes as held and some as marked
        history.held_classes = [history.dates[0], history.dates[1], history.dates[2], history.dates[3]]
        history.marked_classes = [history.dates[0], history.dates[2]]
        expected_marked = [d.strftime(DATE_FMT) for d in history.marked_classes]
        expected_unmarked = [d.strftime(DATE_FMT) for d in history.held_classes if d not in history.marked_classes]

        marked = get_marked_classes(history, "")
        unmarked = get_unmarked_classes(history, "")

        self.assertEqual(marked, expected_marked)
        self.assertEqual(unmarked, expected_unmarked)

    def test_save_and_load(self) -> None:
        """Test saving and loading history with custom paths."""
        with TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "test_history.json"
            history = create_test_history(
                orientation_date=datetime(2025, 1, 6),  # Monday
                weeks=5,
                class_days=[0, 1, 2]  # Mon, Tue, Wed
            )
            result = sync_classes(history)
            assert result.is_ok()
            history.held_classes = [history.dates[0]]

            result = save_test_history(history, test_path)
            assert result.is_ok()
            loaded = load_test_history(test_path).unwrap()

            self.assertEqual(len(loaded.held_classes), 1)
            self.assertEqual(loaded.weeks, history.weeks)
            self.assertEqual(loaded.class_days, history.class_days)


if __name__ == "__main__":
    _ = unittest.main()
