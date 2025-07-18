import unittest

from pylms.lms.utils.find import find_col, find_count
from pylms.utils import DataStream, paths, read_data


class FindTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = DataStream(read_data(paths.get_paths_excel()["Result"]))
        # note that these expected values are based off the actual data contained at the path `paths.get_paths_excel()["Result"]` at the time of testing.
        # When carrying new tests modifies these values to reflect the current result data at `paths.get_paths_excel()["Result"]` before continuing
        self.expected = [
            "Assessment [40%]",
            "Attendance [100%]",
            "Attendance [8]",
        ]
        self.expected_count = 8

    def test_find(self) -> None:
        name = find_col(self.data, "Assessment", "Score")
        self.assertEqual(name, self.expected[0])
        name = find_col(self.data, "Attendance", "Score")
        self.assertEqual(name, self.expected[1])
        name = find_col(self.data, "Attendance", "Count")
        self.assertEqual(name, self.expected[2])

    def test_find_count(self) -> None:
        name = find_col(self.data, "Attendance", "Count")
        count = find_count(name)
        self.assertEqual(count, self.expected_count)


if __name__ == "__main__":
    unittest.main()
