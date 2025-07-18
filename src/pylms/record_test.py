import unittest
from pylms.record import RecordStatus, retrieve_record


class RecordTest(unittest.TestCase):
    def test_retrieve_record(self) -> None:
        sample: list[str] = [
            "Present",
            "Excused",
            "Absent",
            "CDS",
            "No Class",
            "I don't know",
            " ",
        ]
        expected: list[RecordStatus] = [
            RecordStatus.PRESENT,
            RecordStatus.EXCUSED,
            RecordStatus.ABSENT,
            RecordStatus.CDS,
            RecordStatus.NO_CLASS,
            RecordStatus.EMPTY,
            RecordStatus.EMPTY,
        ]
        for item, expected_result in zip(sample, expected):
            self.assertEqual(expected_result, retrieve_record(item))