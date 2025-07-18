import unittest
from pathlib import Path
from unittest import TestCase
from uuid import UUID

import pandas as pd

from pylms.cache.cache import cache_for_cmd
from pylms.constants import CACHE_ID
from pylms.data_ops import load
from pylms.forms.retrieve_form_api import retrieve_cds_form
from pylms.rollcall import cds
from pylms.utils import DataStream, paths, read_csv


class TestCopyData(TestCase):
    def setUp(self) -> None:
        self.ds = load()

    def tearDown(self) -> None:
        return None

    def test_copy_data(self) -> None:
        cds_form_stream: DataStream[pd.DataFrame] | None = retrieve_cds_form()
        if cds_form_stream is not None:
            self.ds = cds(self.ds, cds_form_stream)
            print("Marked CDS Records")
        cache_for_cmd("Mark CDS Days for a Class.")
        cache_record: pd.DataFrame = read_csv(paths.get_metadata_path())
        snapshot_id = cache_record[CACHE_ID].loc[0]
        snapshot_path: Path = paths.get_snapshot_path(UUID(hex=snapshot_id, version=4))
        self.assertTrue(snapshot_path.exists())


if __name__ == "__main__":
    unittest.main()