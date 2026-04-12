"""Unit tests for history/update.py module."""

import unittest
from datetime import datetime
from unittest import TestCase

from ..constants import DATE_FMT
from ..models import CDSFormInfo, UpdateFormInfo
from .classes import sync_classes
from .test_fixtures import create_test_history
from .update import (
    add_cds_form,
    add_held_class,
    add_marked_class,
    add_update_form,
)


class TestAddHeldClass(TestCase):
    """Tests for add_held_class function."""

    def test_add_held_class_single(self) -> None:
        """Test adding single held class."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2],  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        date = history.dates[0].strftime(DATE_FMT)

        result = add_held_class(history, date)

        self.assertTrue(result.is_ok())
        self.assertIn(date, history.held_classes)

    def test_add_held_class_duplicate(self) -> None:
        """Test adding duplicate held class."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2],  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        date = history.dates[0]
        date_str = date.strftime(DATE_FMT)

        result = add_held_class(history, date_str)

        self.assertTrue(result.is_ok())
        self.assertEqual(history.held_classes.count(date), 1)


class TestAddMarkedClass(TestCase):
    """Tests for add_marked_class function."""

    def test_add_marked_class_single(self) -> None:
        """Test adding single marked class."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2],  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        date = history.dates[0].strftime(DATE_FMT)

        result = add_marked_class(history, date)

        self.assertTrue(result.is_ok())
        self.assertIn(date, history.marked_classes)


class TestAddCDSForm(TestCase):
    """Tests for add_cds_form function."""

    def test_add_cds_form_valid(self) -> None:
        """Test adding valid CDS form."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2],  # Mon, Tue, Wed
        )
        form = CDSFormInfo(
            name="CDS Form 1",
            title="CDS Attendance",
            url="https://forms.google.com/cds",
            uuid="cds-uuid-123",
            timestamp="2025-01-08 10:00:00",
        )

        add_cds_form(history, form)

        self.assertIn(form, history.cds_forms)


class TestAddUpdateForm(TestCase):
    """Tests for add_update_form function."""

    def test_add_update_form_valid(self) -> None:
        """Test adding valid update form."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2],  # Mon, Tue, Wed
        )
        form = UpdateFormInfo(
            week_num=1,
            year_num=2025,
            name="Update Form 1",
            title="Update Attendance",
            dates=["08/01/2025", "10/01/2025"],
            url="https://forms.google.com/update",
            uuid="update-uuid-123",
            timestamp="2025-01-08 10:00:00",
        )

        add_update_form(history, form)

        self.assertIn(form, history.update_forms)


if __name__ == "__main__":
    unittest.main()
