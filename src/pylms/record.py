import unittest
from enum import StrEnum


class RecordStatus(StrEnum):
    PRESENT = "Present"
    EXCUSED = "Excused"
    CDS = "CDS"
    ABSENT = "Absent"
    NO_CLASS = "No Class"
    EMPTY = " "


def retrieve_record(record_str: str) -> RecordStatus:
    record_str = record_str.title()
    match record_str:
        case "Present":
            return RecordStatus.PRESENT
        case "Excused":
            return RecordStatus.EXCUSED
        case "CDS":
            return RecordStatus.CDS
        case "Absent":
            return RecordStatus.ABSENT
        case "No Class":
            return RecordStatus.NO_CLASS
        case _:
            return RecordStatus.EMPTY


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
