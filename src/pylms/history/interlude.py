from datetime import datetime, timedelta
from typing import Self, overload

from ..constants import DATE_FMT
from ..date import to_date
from ..errors import Result, eprint


class Interlude:
    """Represents a break period in the course schedule."""
    
    @classmethod
    def new(cls, start: datetime, determinant: int | datetime) -> Result[Self]:
        """Create new Interlude with start date and end determinant.
        
        Args:
            start (datetime): Start date of interlude.
            determinant (int | datetime): Either number of days or end date.
            
        Returns:
            Result[Self]: Success with Interlude instance or error message.
        """
        if isinstance(determinant, datetime):
            end = determinant
            if end < start:
                msg = f"Interlude End {end.strftime(DATE_FMT)} must be ahead of Interlude Start {start.strftime(DATE_FMT)}"
                eprint(msg)
                return Result.err(msg)
            return Result.ok(cls(start, end))

        if determinant <= 0:
            msg = f"Days of interlude must be greater than 0 not {determinant}"
            eprint(msg)
            return Result.err(msg)

        end = start + timedelta(days=determinant)
        return Result.ok(cls(start, end))

    def __init__(self, start: datetime, end: datetime) -> None:
        """Initialize Interlude with start and end dates.
        
        Args:
            start (datetime): Start date of interlude.
            end (datetime): End date of interlude.
        """
        self.start: datetime = start
        self.shift: int = (end - start).days
        self.end: datetime = end

    def to_dict(self) -> dict[str, str]:
        """Convert Interlude to dictionary representation.
        
        Returns:
            dict[str, str]: Dictionary with start, shift, and end keys.
        """
        return {
            "start": to_date(self.start).unwrap(),
            "shift": str(self.shift),
            "end": to_date(self.end).unwrap(),
        }

    @classmethod
    def from_dict(cls, value: dict[str, str | None]) -> Result[Self]:
        """Create Interlude from dictionary representation.
        
        Args:
            value (dict[str, str | None]): Dictionary with start and shift keys.
            
        Returns:
            Result[Self]: Success with Interlude instance or error message.
        """
        if "start" in value and "shift" in value:
            start = value["start"]
            if start is None:
                msg = "start cannot be None"
                eprint(msg)
                return Result.err(msg)

            try:
                start = datetime.strptime(start, DATE_FMT)
            except Exception:
                msg = f"failed to parse Interlude Start: '{start}' in the format: {DATE_FMT}"
                eprint(msg)
                return Result.err(msg)

            shift = value["shift"]
            if shift is None:
                msg = "shift cannot be None"
                eprint(msg)
                return Result.err(msg)

            try:
                shift = int(shift)
            except ValueError:
                msg = f"failed to parse Interlude Shift: '{shift}' as an int"
                eprint(msg)
                return Result.err(msg)

            return cls.new(start, shift)

        msg = (
            "Dictionary must contain keys 'start' and 'shift' to be parsed to Interlude"
        )
        eprint(msg)
        return Result.err(msg)
