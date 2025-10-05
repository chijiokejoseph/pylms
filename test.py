from pathlib import Path

from pylms.cli.errors import ForcedExitError


TEST_PATH: Path = Path("C:\\Users\\Justin\\OneDrive\\NCAIR\\Cohorts\\Cohort 29").resolve()


print(TEST_PATH.is_dir())

error = ForcedExitError("This is a test error")

match error:
    case ForcedExitError():
        print("Caught ForcedExitError")
    case _:
        print("Caught some other error")