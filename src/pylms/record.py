from enum import StrEnum


class RecordStatus(StrEnum):
    PRESENT = "Present"
    EXCUSED = "Excused"
    CDS = "CDS"
    ABSENT = "Absent"
    NO_CLASS = "No Class"
    EMPTY = " "


def retrieve_record(record_str: str) -> RecordStatus:
    match str(record_str):
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
