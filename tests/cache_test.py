import unittest
from pathlib import Path
from typing import final, override
from unittest import TestCase
from uuid import UUID

from pylms import paths
from pylms.cache.cache import cache_for_cmd
from pylms.constants import CACHE_ID
from pylms.data import read
from pylms.data_service import load
from pylms.form_retrieve import retrieve_cds_form
from pylms.history import load_history
from pylms.rollcall import record_cds


@final
class TestCopyData(TestCase):
    """
    Unit test class for testing the cache_for_cmd functionality.

    This test class sets up the necessary data and history, performs operations to mark CDS records,
    caches the command, and verifies that the snapshot path exists as expected.
    """

    @override
    def setUp(self) -> None:
        """
        Set up test environment by loading data and history.

        :return: (None) - This method does not return a value.
        :rtype: None
        """
        self.ds = load()  # pyright: ignore[reportUninitializedInstanceVariable]
        self.history = load_history()  # pyright: ignore[reportUninitializedInstanceVariable]

    def test_copy_data(self) -> None:
        """
        Test the cache_for_cmd function by marking CDS days for a class and verifying snapshot creation.

        :return: (None) - This test method does not return a value.
        :rtype: None
        """
        ds = self.ds.unwrap()
        history = self.history.unwrap()
        result = retrieve_cds_form(history)
        if result.is_err():
            result.print_if_err()
            return
        cds_form_stream, _ = result.unwrap()
        record_cds(ds, cds_form_stream)
        print("Marked CDS Records")

        # Cache the command with a description
        result = cache_for_cmd("Mark CDS Days for a Class.")

        if result.is_err():
            return

        # Read the cache record metadata
        cache_record = read(paths.get_metadata_path())

        if cache_record.is_err():
            cache_record.print_if_err()
            return

        cache_record = cache_record.unwrap()

        # Extract the snapshot ID from the cache record
        snapshot_id = cache_record[CACHE_ID].loc[0]

        # Get the snapshot path using the snapshot ID
        snapshot_path: Path = paths.get_snapshot_path(UUID(hex=snapshot_id, version=4))

        # Assert that the snapshot path exists
        self.assertTrue(snapshot_path.exists())


if __name__ == "__main__":
    _ = unittest.main()
