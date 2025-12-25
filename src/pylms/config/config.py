from abc import ABC, abstractmethod
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Self, cast, override


class TomlProtocol(ABC):
    """Protocol for TOML-backed configuration objects.

    Implementing classes must provide ways to construct a default instance,
    create an instance from a generic value (typically parsed TOML), and
    serialize the instance to a dictionary suitable for TOML serialization.

    This class is used as an abstract base to document the required methods.
    """

    @classmethod
    @abstractmethod
    def default(cls) -> Self:
        """Create and return a default instance.

        Returns:
            Self: A default instance of the implementing class.
        """
        pass

    @classmethod
    @abstractmethod
    def from_value(cls, value_in: Any) -> Self:
        """Create an instance from a generic value.

        Args:
            value_in: A parsed value (for example, from toml parsing) from which
                the implementation should construct an instance.

        Returns:
            Self: The constructed instance.
        """
        pass

    @abstractmethod
    def to_dict(self) -> Mapping[str, object]:
        """Serialize the instance to a dictionary.

        Returns:
            Mapping[str, object]: A dictionary representation suitable for
            TOML serialization.
        """
        pass


class TomlSettings(TomlProtocol):
    """Settings portion of the application's TOML configuration.

    This object holds simple, user-editable settings such as the data
    directory path and the configured course name.

    Attributes:
        data_dir (str): Directory path used by the application to store data.
        course_name (str): Human-readable name of the course or instance.
    """

    def __init__(self, data_dir: str, course_name: str) -> None:
        """Initialize settings.

        Args:
            data_dir: Directory path for data storage.
            course_name: Course name.
        """
        self.data_dir: str = data_dir
        self.course_name: str = course_name

    @classmethod
    @override
    def default(cls) -> Self:
        """Return a default settings instance.

        The default has empty strings for both `data_dir` and `course_name`.

        Returns:
            Self: Default `TomlSettings`.
        """
        return cls(data_dir="", course_name="")

    @classmethod
    @override
    def from_value(cls, value_in: Any) -> Self:
        """Construct settings from a generic mapping.

        The implementation expects a mapping-like object (as produced by a TOML
        parser). Missing or invalid fields are coerced to sensible defaults.

        Args:
            value_in: Parsed value (typically a dict) from which to build settings.

        Returns:
            Self: A `TomlSettings` instance.
        """
        default = cls(data_dir="", course_name="")
        # If input is not a dict we cannot extract fields — return defaults.
        if not isinstance(value_in, dict):
            return default

        # The code below iterates the dict in insertion order; we intentionally
        # read keys/values separately and zip them to preserve that order while
        # performing light type coercion. This mirrors the original behavior
        # and avoids KeyError if unexpected keys are present.
        keys = list(value_in.keys())
        values = list(value_in.values())

        # Empty mappings produce the default object.
        if len(keys) == 0:
            return default
        if len(values) == 0:
            return default

        obj = default
        # Assign values to attributes if keys match expected fields.
        # We guard each assignment with an isinstance check to ensure the stored
        # attribute remains a string; invalid types fall back to empty string.
        for key, value in zip(keys, values):
            if key == "data_dir":
                # Accept only string values for `data_dir`.
                obj.data_dir = value if isinstance(value, str) else ""
            if key == "course_name":
                # Accept only string values for `course_name`.
                obj.course_name = value if isinstance(value, str) else ""
        return obj

    @override
    def to_dict(self) -> dict[str, str]:
        """Serialize settings to a dictionary.

        Returns:
            dict[str, str]: Dictionary with keys `data_dir` and `course_name`.
        """
        return {"data_dir": self.data_dir, "course_name": self.course_name}


class TomlState(TomlProtocol):
    """State portion of the application's TOML configuration.

    The state tracks historical or current boolean flags (for example, whether
    the application is 'open' or 'closed').

    Attributes:
        open (list[bool]): Ordered list of boolean states (True=open, False=closed).
    """

    open: list[bool]

    def __init__(self, open_in: list[bool]) -> None:
        """Initialize state.

        Args:
            open_in: List of boolean values representing the open/closed history.
        """
        # Store the provided list directly — it represents the history of opens/closes.
        self.open = open_in

    @classmethod
    @override
    def default(cls) -> Self:
        """Return a default state instance.

        The default contains an empty `open` list.

        Returns:
            Self: Default `TomlState`.
        """
        return cls(open_in=[])

    @classmethod
    @override
    def from_value(cls, value_in: Any) -> Self:
        """Construct state from a generic mapping.

        The function looks for an `open` key whose value is a list of booleans.
        Invalid or missing data results in the default state being returned.

        Args:
            value_in: Parsed value (typically a dict) from which to build state.

        Returns:
            Self: A `TomlState` instance.
        """
        default = cls(open_in=[])
        # Only mappings can contain the 'open' key we expect.
        if not isinstance(value_in, dict):
            return default

        # Iterate to find a valid 'open' entry.
        for key, value in value_in.items():
            if key != "open":
                # Skip unrelated keys; we don't treat them as errors here.
                continue
            # Value must be a list to represent history.
            if not isinstance(value, list):
                continue
            # We require a non-empty list of booleans to consider it valid.
            # This prevents accidental acceptance of malformed data such as
            # lists of strings or mixed types.
            if len(value) == 0 or not all(
                isinstance(each_value, bool) for each_value in value
            ):
                continue
            # Value validated — cast and return the new state instance.
            return cls(open_in=cast(list[bool], value))
        # No valid 'open' key found; return default state.
        return default

    @override
    def to_dict(self) -> Mapping[str, list[bool]]:
        """Serialize state to a dictionary.

        Returns:
            Mapping[str, list[bool]]: Dictionary with key `open` holding the list of booleans.
        """
        return {"open": self.open}


class Config(TomlProtocol):
    """Top-level configuration object combining settings and state.

    This object is the in-memory representation of the TOML configuration
    used by the application. It exposes convenience methods for common
    operations such as checking if the application is open and manipulating
    the stored settings.

    Attributes:
        settings (TomlSettings): Settings sub-object.
        state (TomlState): State sub-object.
    """

    settings: TomlSettings
    state: TomlState

    def __init__(self, settings: TomlSettings, state: TomlState) -> None:
        """Initialize the configuration.

        Args:
            settings: TomlSettings instance.
            state: TomlState instance.
        """
        # Straightforward composition: store sub-objects on the instance.
        self.settings = settings
        self.state = state

    @classmethod
    @override
    def default(cls) -> Self:
        """Create a default configuration.

        Returns:
            Self: `Config` constructed from default `TomlSettings` and `TomlState`.
        """
        return cls(settings=TomlSettings.default(), state=TomlState.default())

    @classmethod
    @override
    def from_value(cls, value_in: Any) -> Self:
        """Construct a `Config` from a generic mapping.

        The function expects a mapping (for example parsed from TOML) and will
        delegate construction of sub-objects to `TomlSettings.from_value` and
        `TomlState.from_value` where appropriate.

        Args:
            value_in: Parsed value (typically a dict).

        Returns:
            Self: A `Config` instance.
        """
        default = cls(settings=TomlSettings.default(), state=TomlState.default())
        # If input is not a mapping, return the default config.
        if not isinstance(value_in, dict):
            return default

        # Walk known top-level keys and delegate to sub-object parsers.
        for key, item in value_in.items():
            match str(key):
                case "settings":
                    # Build settings from the nested mapping (safe coercions happen there).
                    default.settings = TomlSettings.from_value(item)
                case "state":
                    # Build state using its own validation rules.
                    default.state = TomlState.from_value(item)
                case _:
                    # Unknown keys are ignored to preserve forward compatibility.
                    pass

        return default

    def from_self(self, other: Self) -> None:
        """Update this config from another `Config`.

        Args:
            other: Another `Config` whose settings and state will be copied into this instance.
        """
        # Perform a shallow copy of references. This method intentionally does
        # not deep-copy to allow callers to replace the whole sub-objects.
        self.settings = other.settings
        self.state = other.state

    @override
    def to_dict(self) -> dict[str, object]:
        """Serialize the configuration to a mapping.

        Returns:
            dict[str, object]: Dictionary with keys `settings` and `state`,
            both of which are themselves serializable mappings.
        """
        return {"settings": self.settings.to_dict(), "state": self.state.to_dict()}

    def is_open(self) -> bool:
        """Return whether the most recent recorded state is open.

        Returns:
            bool: True if the latest recorded state is open, False otherwise.

        Raises:
            IndexError: If the state history is empty.
        """
        # Access the last element of the history list. Let Python raise IndexError
        # naturally if the list is empty — callers can catch it if needed.
        return self.state.open[-1]

    def has_data_dir(self) -> bool:
        """Determine whether a configured data directory exists.

        Returns:
            bool: True if `settings.data_dir` points to an existing, non-empty
            path; otherwise False.
        """
        # Convert setting into a Path and test for existence. Comparing to an
        # empty Path avoids treating an empty string as an existing path.
        path = Path(self.settings.data_dir)
        return path.exists() and path != Path("")

    def has_course_name(self) -> bool:
        """Return whether a course name has been configured.

        Returns:
            bool: True if `settings.course_name` is a non-empty string.
        """
        # A simple non-empty string check suffices here.
        return self.settings.course_name != ""

    def open(self) -> None:
        """Mark the configuration as open.

        This appends a True value to the state's `open` history list.
        """
        # Record the new state; history is preserved.
        self.state.open.append(True)

    def close(self) -> None:
        """Mark the configuration as closed.

        This appends a False value to the state's `open` history list.
        """
        # Record the closed state; callers may read history or the last item.
        self.state.open.append(False)

    def reset_data_dir(self) -> None:
        """Clear the configured data directory.

        After calling this, `settings.data_dir` will be an empty string.
        """
        # Clear the stored path value. Persistence (if any) is the caller's responsibility.
        self.settings.data_dir = ""

    def reset_course_name(self) -> None:
        """Clear the configured course name.

        After calling this, `settings.course_name` will be an empty string.
        """
        # Clear the stored name.
        self.settings.course_name = ""

    @property
    def data_dir(self) -> str:
        """Return the configured data directory path.

        Returns:
            str: The `settings.data_dir` value.
        """
        return self.settings.data_dir

    @property
    def open_(self) -> list[bool]:
        """Return the state's open history.

        Returns:
            list[bool]: The `state.open` list recording open/closed history.
        """
        # Returning the list directly lets callers inspect history; modifications
        # to this list will affect the Config instance (intentional).
        return self.state.open
