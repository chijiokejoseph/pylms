from .assessment import collate_assessment
from .attendance import collate_attendance
from .awardees_fast_track import collate_fast_track
from .awardees_merged import collate_merge
from .awardees_merit import collate_merit
from .project import collate_project
from .recollate import recollate
from .result import collate_result

__all__ = [
    "collate_attendance",
    "collate_assessment",
    "collate_project",
    "collate_fast_track",
    "collate_merit",
    "collate_merge",
    "collate_result",
    "recollate",
]
