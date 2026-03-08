"""Unit tests for history/groups.py module."""

import unittest
from datetime import datetime
from unittest import TestCase

from .groups import get_num_groups
from .test_fixtures import create_test_history


class TestGroups(TestCase):
    """Tests for groups functions."""

    def test_get_num_groups(self) -> None:
        """Test getting number of groups."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        history.group = (True, 5)

        num = get_num_groups(history)

        self.assertEqual(num, 5)


if __name__ == "__main__":
    _ = unittest.main()
