"""Unit tests for history/classes.py module."""

import unittest
from datetime import datetime
from unittest import TestCase

from .classes import extend_weeks, replan_weeks, set_class_days, sync_classes
from .interlude import Interlude
from .test_fixtures import create_test_history


class TestSyncClasses(TestCase):
    """Tests for sync_classes function."""

    def test_sync_classes_basic(self) -> None:
        """Test basic class synchronization without interlude."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )

        result = sync_classes(history)

        self.assertTrue(result.is_ok())
        self.assertEqual(len(history.dates), 15)
        self.assertTrue(history._updated)  # pyright: ignore[reportPrivateUsage]

    def test_sync_classes_with_interlude(self) -> None:
        """Test class synchronization with interlude."""
        interlude = Interlude(start=datetime(2025, 1, 20), end=datetime(2025, 1, 27))
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2],  # Mon, Tue, Wed
            interlude=interlude
        )

        result = sync_classes(history)

        self.assertTrue(result.is_ok())
        for date in history.dates:
            self.assertFalse(interlude.start < date < interlude.end)

    def test_sync_classes_invalid_class_days(self) -> None:
        """Test sync_classes with invalid number of class days."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1]  # Only 2 days
        )

        result = sync_classes(history)

        self.assertTrue(result.is_err())

    def test_sync_classes_no_orientation_date(self) -> None:
        """Test sync_classes without orientation date."""
        history = create_test_history(
            orientation_date=None,
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )

        result = sync_classes(history)

        self.assertTrue(result.is_err())


class TestSetClassDays(TestCase):
    """Tests for set_class_days function."""

    def test_set_class_days_with_integers_and_start(self) -> None:
        """Test setting class days with integer indices and start."""
        history = create_test_history()

        result = set_class_days(history, [1, 3, 5], start=1)

        self.assertTrue(result.is_ok())
        self.assertEqual(history.class_days, [0, 2, 4])

    def test_set_class_days_with_strings(self) -> None:
        """Test setting class days with weekday names."""
        history = create_test_history()

        result = set_class_days(history, ["Monday", "Wednesday", "Friday"], start=None)

        self.assertTrue(result.is_ok())
        self.assertEqual(history.class_days, [0, 2, 4])

    def test_set_class_days_invalid_count(self) -> None:
        """Test setting class days with wrong number of days."""
        history = create_test_history()

        result = set_class_days(history, [0, 2], start=0)

        self.assertTrue(result.is_err())

    def test_set_class_days_duplicate_days(self) -> None:
        """Test setting class days with duplicate values."""
        history = create_test_history()

        result = set_class_days(history, [1, 1, 3], start=1)

        self.assertTrue(result.is_err())


class TestExtendWeeks(TestCase):
    """Tests for extend_weeks function."""

    def test_extend_weeks_positive(self) -> None:
        """Test extending weeks with positive value."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=10,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )

        result = extend_weeks(history, 2)

        self.assertTrue(result.is_ok())
        self.assertEqual(history.weeks, 12)

    def test_extend_weeks_invalid(self) -> None:
        """Test extending weeks with invalid value."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=10,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )

        result = extend_weeks(history, 0)

        self.assertTrue(result.is_err())


class TestReplanWeeks(TestCase):
    """Tests for replan_weeks function."""

    def test_replan_weeks_valid(self) -> None:
        """Test replanning weeks with valid value."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )

        result = replan_weeks(history, 10)

        self.assertTrue(result.is_ok())
        self.assertEqual(history.weeks, 10)

    def test_replan_weeks_invalid(self) -> None:
        """Test replanning weeks with invalid value."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=10,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )

        result = replan_weeks(history, 1)

        self.assertTrue(result.is_err())


if __name__ == "__main__":
    _ = unittest.main()