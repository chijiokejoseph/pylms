from abc import ABC, abstractmethod
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Self, cast, override


class TomlProtocol(ABC):
    """
    Abstract base class defining the protocol for TOML configuration objects.

    This protocol requires implementing classes to provide methods for:
    - Creating a default instance
    - Creating an instance from a generic value
    - Converting the instance to a dictionary representation

    """

    @classmethod
    @abstractmethod
    def default(cls) -> Self:
        """
        Create and return a default instance of the implementing class.

        Returns:
             Self: A default instance of the class.
        """
        pass

    @classmethod
    @abstractmethod
    def from_value(cls, value_in: Any) -> Self:
        """
        Create an instance of the class from a generic input value.

        Args:
            value_in (Any): The input value to convert from

        Returns:
            Self: An instance of the class created from the input value
        """
        pass

    @abstractmethod
    def to_dict(self) -> Mapping[str, object]:
        """
        Convert the instance into a dictionary representation.

        Return:
            dict[str, object]: A dictionary representing the instance
        """
        pass


class TomlSettings(TomlProtocol):
    """
    Represents the settings configuration for the TOML file.

    This class holds configuration details such as the data directory path
    and the course name. It provides methods to create default settings,
    instantiate from a generic value, and convert the settings to a dictionary.

    Vars:
        data_dir (str): The directory path for data storage.
        course_name (str): The name of the course.
    """

    def __init__(self, data_dir: str, course_name: str) -> None:
        """
        Initialize `TomlSettings` with data directory and course name.

        Args:
            data_dir (str): The directory path for data storage.
            course_name (str): The name of the course.
        """
        self.data_dir: str = data_dir
        self.course_name: str = course_name

    @classmethod
    @override
    def default(cls) -> Self:
        """
        Create a default `TomlSettings` instance with empty `data_dir` and `course_name`.

        Returns:
            Self: A default instance of `TomlSettings`
        """
        return cls(data_dir="", course_name="")

    @classmethod
    @override
    def from_value(cls, value_in: Any) -> Self:
        """
        Create a TomlSettings instance from a generic input value.

        :param value_in: (Any) - The input value to convert from.

        :return: (Self) - An instance of TomlSettings created from the input value.
        :rtype: Self
        """
        default = cls(data_dir="", course_name="")
        # Return default if input is not a dictionary
        if not isinstance(value_in, dict):
            return default
        # Get dictionary keys and values as lists
        keys = list(value_in.keys())
        values = list(value_in.values())
        # Return default if dictionary is empty
        if len(keys) == 0:
            return default
        if len(values) == 0:
            return default
        obj = default
        # Assign values to attributes if keys match expected fields
        for key, value in zip(keys, values):
            if key == "data_dir":
                obj.data_dir = value if isinstance(value, str) else ""
            if key == "course_name":
                obj.course_name = value if isinstance(value, str) else ""
        return obj

    @override
    def to_dict(self) -> dict[str, str]:
        """
        Convert the TomlSettings instance into a dictionary representation.

        :return: (dict[str, str]) - A dictionary with keys 'data_dir' and 'course_name'.
        :rtype: dict[str, str]
        """
        return {"data_dir": self.data_dir, "course_name": self.course_name}


class TomlState(TomlProtocol):
    """
    Represents the state configuration for the TOML file.

    This class holds a list of boolean values indicating open states.
    It provides methods to create default state, instantiate from a generic value,
    and convert the state to a dictionary.

    :ivar open: (list[bool]) - A list indicating open states.
    """

    open: list[bool]

    def __init__(self, open_in: list[bool]) -> None:
        """
        Initialize TomlState with a list of boolean open states.

        :param open_in: (list[bool]) - A list indicating open states.
        """
        # Assign the list of open states to the instance variable
        self.open = open_in

    @classmethod
    @override
    def default(cls) -> Self:
        """
        Create a default TomlState instance with an empty open list.

        :return: (Self) - A default instance of TomlState.
        :rtype: Self
        """
        # Return an instance with an empty list for open states
        return cls(open_in=[])

    @classmethod
    @override
    def from_value(cls, value_in: Any) -> Self:
        """
        Create a TomlState instance from a generic input value.

        :param value_in: (Any) - The input value to convert from.

        :return: (Self) - An instance of TomlState created from the input value.
        :rtype: Self
        """
        default = cls(open_in=[])
        # Return default if input is not a dictionary
        if not isinstance(value_in, dict):
            return default
        # Iterate over dictionary items to find 'open' key with valid list of bools
        for key, value in value_in.items():
            if key != "open":
                continue
            # Skip if value is not a list
            if not isinstance(value, list):
                continue
            # Skip if list is empty or first element is not a bool
            if len(value) == 0 or not all(
                isinstance(each_value, bool) for each_value in value
            ):
                continue
            # Cast the list to list of bool and return new instance
            return cls(open_in=cast(list[bool], value))
        # Return default if no valid 'open' key found
        return default

    @override
    def to_dict(self) -> Mapping[str, list[bool]]:
        """
        Convert the TomlState instance into a dictionary representation.

        :return: (dict[str, list[bool]]) - A dictionary with key 'open' and list of boolean values.
        :rtype: dict[str, list[bool]]
        """
        # Return dictionary representation of the open states
        return {"open": self.open}


class Config(TomlProtocol):
    """
    Represents the overall configuration combining settings and state.

    This class encapsulates the TomlSettings and TomlState instances,
    providing methods to create default configuration, instantiate from a generic value,
    update from another instance, convert to dictionary, and manage open state and data attributes.

    :param settings: (TomlSettings) - The settings configuration.
    :type settings: TomlSettings
    :param state: (TomlState) - The state configuration.
    :type state: TomlState

    :return: (Config) - An instance of the Config class.
    """

    settings: TomlSettings
    state: TomlState

    def __init__(self, settings: TomlSettings, state: TomlState) -> None:
        """
        Initialize Config with settings and state.

        :param settings: (TomlSettings) - The settings configuration.
        :type settings: TomlSettings
        :param state: (TomlState) - The state configuration.
        :type state: TomlState

        :return: (None) - returns None.
        :rtype: None
        """
        # Assign the settings and state to the instance variables
        self.settings = settings
        self.state = state

    @classmethod
    @override
    def default(cls) -> Self:
        """
        Create a default Config instance with default settings and state.

        :return: (Self) - A default instance of Config.
        :rtype: Self
        """
        # Return a new Config instance with default settings and state
        return cls(settings=TomlSettings.default(), state=TomlState.default())

    @classmethod
    @override
    def from_value(cls, value_in: Any) -> Self:
        """
        Create a Config instance from a generic input value.

        :param value_in: (Any) - The input value to convert from.
        :type value_in: Any

        :return: (Self) - An instance of Config created from the input value.
        :rtype: Self
        """
        default = cls(settings=TomlSettings.default(), state=TomlState.default())
        # Return default if input is not a dictionary
        if not isinstance(value_in, dict):
            return default
        # Iterate over dictionary items and update settings and state accordingly
        for key, item in value_in.items():
            match str(key):
                case "settings":
                    default.settings = TomlSettings.from_value(item)
                case "state":
                    default.state = TomlState.from_value(item)
                case _:
                    pass

        return default

    def from_self(self, other: Self) -> None:
        """
        Update the current Config instance from another Config instance.

        :param other: (Self) - Another Config instance to copy from.
        :type other: Self

        :return: (None) - returns None.
        :rtype: None
        """
        # Copy settings and state from the other instance
        self.settings = other.settings
        self.state = other.state

    @override
    def to_dict(self) -> dict[str, object]:
        """
        Convert the Config instance into a dictionary representation.

        :return: (dict) - A dictionary with keys 'settings' and 'state'.
        :rtype: dict
        """
        # Return dictionary representation of settings and state
        return {"settings": self.settings.to_dict(), "state": self.state.to_dict()}

    def is_open(self) -> bool:
        """
        Check if the latest state is open.

        :return: (bool) - True if the last state is open, False otherwise.
        :rtype: bool
        """
        # Return the last value in the open state list
        return self.state.open[-1]

    def has_data_dir(self) -> bool:
        """
        Check if the data directory exists and is not empty.

        :return: (bool) - True if data directory exists and is not empty, False otherwise.
        :rtype: bool
        """
        # Check if the data directory path exists and is not empty
        path = Path(self.settings.data_dir)
        return path.exists() and path != Path("")

    def has_course_name(self) -> bool:
        """
        Check if the course name is set (non-empty).

        :return: (bool) - True if course name is not empty, False otherwise.
        :rtype: bool
        """
        # Return True if course name is not an empty string
        return self.settings.course_name != ""

    def open(self) -> None:
        """
        Append True to the open state list indicating an open state.

        :return: (None) - returns None.
        :rtype: None
        """
        # Append True to the open list to indicate open state
        self.state.open.append(True)

    def close(self) -> None:
        """
        Append False to the open state list indicating a closed state.

        :return: (None) - returns None.
        :rtype: None
        """
        # Append False to the open list to indicate closed state
        self.state.open.append(False)

    def reset_data_dir(self) -> None:
        """
        Reset the data directory to an empty string.

        :return: (None) - returns None.
        :rtype: None
        """
        # Reset the data directory string to empty
        self.settings.data_dir = ""

    def reset_course_name(self) -> None:
        """
        Reset the course name to an empty string.

        :return: (None) - returns None.
        :rtype: None
        """
        # Reset the course name string to empty
        self.settings.course_name = ""

    @property
    def data_dir(self) -> str:
        """
        Get the current data directory.

        :return: (str) - The data directory path.
        :rtype: str
        """
        # Return the data directory string
        return self.settings.data_dir

    @property
    def open_(self) -> list[bool]:
        """
        Get the list of open states.

        :return: (list[bool]) - The list of open states.
        :rtype: list[bool]
        """
        # Return the list of open states
        return self.state.open
