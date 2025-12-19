import unittest
from typing import final, override

from pylms import paths
from pylms.data import DataStream, read
from pylms.result_utils import find_col, find_count


@final
class FindTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        data = read(paths.get_paths_excel()["Result"]).unwrap()
        self.data = DataStream(data)  # pyright: ignore [reportUninitializedInstanceVariable]

        # note that these expected values are based off the actual data contained at the path `paths.get_paths_excel()["Result"]` at the time of testing.
        # When carrying new tests modifies these values to reflect the current result data at `paths.get_paths_excel()["Result"]` before continuing
        self.expected = [  # pyright: ignore [reportUninitializedInstanceVariable]
            "Assessment [40%]",
            "Attendance [100%]",
            "Attendance [8]",
        ]
        self.expected_count = 8  # pyright: ignore [reportUninitializedInstanceVariable]

    def test_find(self) -> None:
        name = find_col(self.data, "Assessment", "Score").unwrap()
        self.assertEqual(name, self.expected[0])
        name = find_col(self.data, "Attendance", "Score").unwrap()
        self.assertEqual(name, self.expected[1])
        name = find_col(self.data, "Attendance", "Count").unwrap()
        self.assertEqual(name, self.expected[2])

    def test_find_count(self) -> None:
        name = find_col(self.data, "Attendance", "Count").unwrap()
        count = find_count(name)
        self.assertEqual(count, self.expected_count)


if __name__ == "__main__":
    _ = unittest.main()
