from enum import IntEnum, auto


class ClassType(IntEnum):
    """Enumeration for class form types."""
    PRESENT = auto()
    EXCUSED = auto()
    
    
class RetrieveType(IntEnum):
    """Enumeration for form retrieval types."""
    CLASS = auto()
    CDS = auto()
    DATA = auto()