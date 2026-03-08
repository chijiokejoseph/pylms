from ..errors import Result
from ..history import History, all_dates
from .select import select
from .selector_type import DateSelector


class DateSink:
    """Container for progressively filtering dates through multiple selectors."""
    
    def __init__(self, history: History) -> None:
        """Initialize DateSink with all dates from history.
        
        Args:
            history (History): History instance containing class information.
        """
        self.history: History = history
        # Initialize with all dates from history
        self.dates: list[str] = all_dates(history, "")

    @classmethod
    def from_history(
        cls, history: History, selector: DateSelector
    ) -> Result["DateSink"]:
        """Create a DateSink from a History object with initial selector applied.
        
        Args:
            history (History): History instance containing class information.
            selector (DateSelector): Initial selector to apply.
            
        Returns:
            Result[DateSink]: Success with DateSink or error.
        """
        # Create new sink instance
        sink = cls(history)
        
        # Apply selector to get filtered dates
        dates = select(history, selector)
        if dates.is_err():
            return dates.propagate()
        
        # Update sink with filtered dates
        dates = dates.unwrap()
        sink.dates = dates
        
        return Result.ok(sink)
