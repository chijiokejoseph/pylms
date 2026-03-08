"""Unit tests for history/new.py module."""

import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from .classes import sync_classes
from .test_fixtures import create_test_history, load_test_history, save_test_history


class TestNew(TestCase):
    """Test cases for history loading functionality."""

    def test_load_history(self) -> None:
        """Test that history can be saved and loaded."""
        with TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "test_history.json"
            history = create_test_history(
                orientation_date=datetime(2025, 1, 6),  # Monday
                weeks=5,
                class_days=[0, 1, 2]  # Mon, Tue, Wed
            )
            result = sync_classes(history)
            assert result.is_ok()

            result = save_test_history(history, test_path)
            assert result.is_ok()
            loaded = load_test_history(test_path)

            self.assertTrue(loaded.is_ok())
            loaded_history = loaded.unwrap()
            self.assertEqual(loaded_history.weeks, 5)
            self.assertEqual(loaded_history.class_days, [0, 1, 2])


if __name__ == "__main__":
    _ = unittest.main()
