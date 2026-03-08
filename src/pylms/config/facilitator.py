from ..cli_utils import verify_gmail, verify_name
from ..errors import Result, eprint


class Facilitator:
    """Store facilitator information.

    Attributes:
        name (str): Facilitator name.
        gmail (str): Facilitator Gmail address.
    """

    def __init__(self, name: str, gmail: str) -> None:
        self.name: str = name
        self.gmail: str = gmail

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary for JSON serialization.

        Returns:
            dict[str, str]: Dictionary with name and gmail.
        """
        return {"name": self.name, "gmail": self.gmail}

    @classmethod
    def build(cls, name: str, gmail: str) -> Result["Facilitator"]:
        """Build Facilitator with validation.

        Args:
            name: Facilitator name.
            gmail: Facilitator Gmail address.

        Returns:
            Result[Facilitator]: Ok with Facilitator instance or Err with message.
        """
        if not verify_name(name):
            msg = f"Invalid name: '{name}'"
            eprint(msg)
            return Result.err(msg)

        if not verify_gmail(gmail):
            msg = f"Invalid Gmail: '{gmail}'"
            eprint(msg)
            return Result.err(msg)

        return Result.ok(cls(name=name, gmail=gmail))

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Result["Facilitator"]:
        """Create Facilitator from dictionary with validation.

        Args:
            data: Dictionary with name and gmail keys.

        Returns:
            Result[Facilitator]: Ok with Facilitator instance or Err with message.
        """
        name = data.get("name")
        gmail = data.get("gmail")

        if name is None or gmail is None:
            msg = "Missing name or gmail in data"
            eprint(msg)
            return Result.err(msg)

        return cls.build(name=name, gmail=gmail)
