import unittest
from pathlib import Path
from unittest import TestCase
from uuid import UUID

import pandas as pd

from pylms.cache.cache import cache_for_cmd
from pylms.constants import CACHE_ID
from pylms.data_ops import load
from pylms.forms.retrieve_form_api import retrieve_cds_form
from pylms.rollcall import record_cds
from pylms.utils import paths, read_csv
from pylms.history import History


class TestCopyData(TestCase):
    """
    Unit test class for testing the cache_for_cmd functionality.

    This test class sets up the necessary data and history, performs operations to mark CDS records,
    caches the command, and verifies that the snapshot path exists as expected.
    """

    def setUp(self) -> None:
        """
        Set up test environment by loading data and history.

        :return: (None) - This method does not return a value.
        :rtype: None
        """
        self.ds = load()
        self.history = History.load()

    def test_copy_data(self) -> None:
        """
        Test the cache_for_cmd function by marking CDS days for a class and verifying snapshot creation.

        :return: (None) - This test method does not return a value.
        :rtype: None
        """
        cds_form_stream, _ = retrieve_cds_form(self.history)
        if cds_form_stream is not None:
            # Record CDS data into the dataset
            self.ds = record_cds(self.ds, cds_form_stream)
            print("Marked CDS Records")

        # Cache the command with a description
        cache_for_cmd("Mark CDS Days for a Class.")

        # Read the cache record metadata
        cache_record: pd.DataFrame = read_csv(paths.get_metadata_path())

        # Extract the snapshot ID from the cache record
        snapshot_id = cache_record[CACHE_ID].loc[0]

        # Get the snapshot path using the snapshot ID
        snapshot_path: Path = paths.get_snapshot_path(UUID(hex=snapshot_id, version=4))

        # Assert that the snapshot path exists
        self.assertTrue(snapshot_path.exists())


if __name__ == "__main__":
    unittest.main()
