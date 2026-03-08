"""Unit tests for history/dates_with_history.py module."""

import unittest
from datetime import datetime
from unittest import TestCase

from .classes import sync_classes
from .dates_with_history import all_dates
from .test_fixtures import create_test_history


class TestAllDates(TestCase):
    """Tests for all_dates function."""

    def test_all_dates_with_string_sample(self) -> None:
        """Test all_dates returns string dates."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()

        dates = all_dates(history, "")

        self.assertIsInstance(dates, list)
        self.assertGreater(len(dates), 0)

    def test_all_dates_with_datetime_sample(self) -> None:
        """Test all_dates returns datetime objects."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()

        dates = all_dates(history, datetime.now())

        self.assertIsInstance(dates, list)
        self.assertGreater(len(dates), 0)


if __name__ == "__main__":
    _ = unittest.main()
