"""Unit tests for history/match_classes.py module."""

from datetime import datetime
from unittest import TestCase

from ..constants import DATE_FMT
from .classes import sync_classes
from .match_classes import match_classes
from .test_fixtures import create_test_history


class TestMatchClasses(TestCase):
    """Tests for match_classes function."""

    def test_match_classes_single_number(self) -> None:
        """Test matching single class number."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        dates = [date.strftime(DATE_FMT) for date in history.dates]

        result = match_classes(history, "1", dates)

        assert result.is_ok()
        matched = result.unwrap()
        self.assertEqual(matched, [dates[0]])

    def test_match_classes_range(self) -> None:
        """Test matching range of class numbers."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        dates = [date.strftime(DATE_FMT) for date in history.dates]

        result = match_classes(history, "1-3", dates)

        assert result.is_ok()
        matched = result.unwrap()
        self.assertEqual(matched, dates[0:3])

    def test_match_classes_comma_separated(self) -> None:
        """Test matching comma-separated class numbers."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        dates = [date.strftime(DATE_FMT) for date in history.dates]

        result = match_classes(history, "1, 3, 5", dates)

        assert result.is_ok()
        matched = result.unwrap()
        self.assertEqual(matched, [dates[0], dates[2], dates[4]])

    def test_match_classes_all(self) -> None:
        """Test matching 'all' keyword."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        dates = [date.strftime(DATE_FMT) for date in history.dates]

        result = match_classes(history, "all", dates)

        assert result.is_ok()
        matched = result.unwrap()
        self.assertEqual(matched, dates)

    def test_match_classes_exact_date(self) -> None:
        """Test matching exact date string."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        dates = [date.strftime(DATE_FMT) for date in history.dates]

        result = match_classes(history, dates[0], dates)

        assert result.is_ok()
        matched = result.unwrap()
        self.assertEqual(matched, [dates[0]])

    def test_match_classes_invalid_number(self) -> None:
        """Test matching invalid class number."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        dates = [date.strftime(DATE_FMT) for date in history.dates]

        result = match_classes(history, "999", dates)

        self.assertTrue(result.is_err())

    def test_match_classes_empty_dates(self) -> None:
        """Test matching with empty dates list."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )

        result = match_classes(history, "1", [])

        self.assertTrue(result.is_err())
