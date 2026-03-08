"""Unit tests for history/update.py module."""

import unittest
from datetime import datetime
from unittest import TestCase

from ..models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from .classes import sync_classes
from .test_fixtures import create_test_history
from .update import (
    add_cds_form,
    add_class_form,
    add_held_class,
    add_marked_class,
    add_recorded_cds_form,
    add_recorded_class_form,
    add_recorded_update_form,
    add_update_form,
)


class TestAddHeldClass(TestCase):
    """Tests for add_held_class function."""

    def test_add_held_class_single(self) -> None:
        """Test adding single held class."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        date = history.dates[0]

        result = add_held_class(history, date)

        self.assertTrue(result.is_ok())
        self.assertIn(date, history.held_classes)

    def test_add_held_class_duplicate(self) -> None:
        """Test adding duplicate held class."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        date = history.dates[0]

        add_held_class(history, date)
        result = add_held_class(history, date)

        self.assertTrue(result.is_ok())
        self.assertEqual(history.held_classes.count(date), 1)


class TestAddMarkedClass(TestCase):
    """Tests for add_marked_class function."""

    def test_add_marked_class_single(self) -> None:
        """Test adding single marked class."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        result = sync_classes(history)
        assert result.is_ok()
        date = history.dates[0]

        result = add_marked_class(history, date)

        self.assertTrue(result.is_ok())
        self.assertIn(date, history.marked_classes)


class TestAddClassForm(TestCase):
    """Tests for add_class_form function."""

    def test_add_class_form_valid(self) -> None:
        """Test adding valid class form."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        form = ClassFormInfo(
            date="08/01/2025",
            name="Class Form 1",
            title="Attendance Form",
            url="https://forms.google.com/test",
            uuid="test-uuid-123",
            timestamp="2025-01-08 10:00:00"
        )

        result = add_class_form(history, form)

        self.assertTrue(result.is_ok())
        self.assertIn(form, history.class_forms)


class TestAddCDSForm(TestCase):
    """Tests for add_cds_form function."""

    def test_add_cds_form_valid(self) -> None:
        """Test adding valid CDS form."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        form = CDSFormInfo(
            name="CDS Form 1",
            title="CDS Attendance",
            url="https://forms.google.com/cds",
            uuid="cds-uuid-123",
            timestamp="2025-01-08 10:00:00"
        )

        result = add_cds_form(history, form)

        self.assertTrue(result.is_ok())
        self.assertIn(form, history.cds_forms)


class TestAddUpdateForm(TestCase):
    """Tests for add_update_form function."""

    def test_add_update_form_valid(self) -> None:
        """Test adding valid update form."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        form = UpdateFormInfo(
            week_num=1,
            year_num=2025,
            name="Update Form 1",
            title="Update Attendance",
            dates=["08/01/2025", "10/01/2025"],
            url="https://forms.google.com/update",
            uuid="update-uuid-123",
            timestamp="2025-01-08 10:00:00"
        )

        result = add_update_form(history, form)

        self.assertTrue(result.is_ok())
        self.assertIn(form, history.update_forms)


class TestRecordForms(TestCase):
    """Tests for record form functions."""

    def test_record_class_form(self) -> None:
        """Test recording class form."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        form = ClassFormInfo(
            date="08/01/2025",
            name="Class Form 1",
            title="Attendance Form",
            url="https://forms.google.com/test",
            uuid="test-uuid-123",
            timestamp="2025-01-08 10:00:00"
        )
        add_class_form(history, form)

        result = add_recorded_class_form(history, form)

        self.assertTrue(result.is_ok())
        self.assertIn(form, history.recorded_class_forms)

    def test_record_cds_form(self) -> None:
        """Test recording CDS form."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        form = CDSFormInfo(
            name="CDS Form 1",
            title="CDS Attendance",
            url="https://forms.google.com/cds",
            uuid="cds-uuid-123",
            timestamp="2025-01-08 10:00:00"
        )
        add_cds_form(history, form)

        result = add_recorded_cds_form(history, form)

        self.assertTrue(result.is_ok())
        self.assertIn(form, history.recorded_cds_forms)

    def test_record_update_form(self) -> None:
        """Test recording update form."""
        history = create_test_history(
            orientation_date=datetime(2025, 1, 6),  # Monday
            weeks=5,
            class_days=[0, 1, 2]  # Mon, Tue, Wed
        )
        form = UpdateFormInfo(
            week_num=1,
            year_num=2025,
            name="Update Form 1",
            title="Update Attendance",
            dates=["08/01/2025", "10/01/2025"],
            url="https://forms.google.com/update",
            uuid="update-uuid-123",
            timestamp="2025-01-08 10:00:00"
        )
        add_update_form(history, form)

        result = add_recorded_update_form(history, form)

        self.assertTrue(result.is_ok())
        self.assertIn(form, history.recorded_update_forms)


if __name__ == "__main__":
    unittest.main()
