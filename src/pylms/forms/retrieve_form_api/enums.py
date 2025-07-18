from enum import IntEnum, auto


class ClassType(IntEnum):
    PRESENT = auto()
    EXCUSED = auto()
    
    
class RetrieveType(IntEnum):
    CLASS = auto()
    CDS = auto()
    DATA = auto()