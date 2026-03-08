"""Pytest runner for all history module unittests."""

import unittest


def test_all_history_unittests() -> None:
    """Discover and run all unittest tests in the history module."""
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=".", pattern="*_test.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    assert result.wasSuccessful(), f"Tests failed: {len(result.failures)} failures, {len(result.errors)} errors"
