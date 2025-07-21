from datetime import datetime
from pathlib import Path
from typing import TypedDict, Callable
import pandas as pd


PARENT_PATH: Path = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH: Path = PARENT_PATH / "data"
STATE_PATH: Path = PARENT_PATH / "state.toml"
SECRETS_PATH: Path = PARENT_PATH / "secrets.json"
HISTORY_PATH: Path = PARENT_PATH / "history.json"
HISTORY_JSON: str = "history.json"
# RollCall Global Data
GLOBAL_RECORD_PATH: Path = PARENT_PATH / "global_record.json"
GLOBAL_RECORD_JSON: str = "global_record.json"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
SCOPES = "https://www.googleapis.com/auth/forms.body"


class Spreadsheets(TypedDict):
    DataStore: Path
    Result: Path
    Registration: Path
    List: Path
    Attendance: Path
    Assessment: Path
    Group: Path
    Project: Path

class Json(TypedDict):
    Classes: Path
    Records: Path
    Update: Path
    CDS: Path
    UpdateForm: Path
    UpdateRecord: Path
    CDSForm: Path
    CDSRecord: Path
    Date: Path


RESULT_UPDATE: str = "Result Update"

type ValidateDataFn = Callable[[pd.DataFrame | pd.Series], bool]


class AwardeesDict(TypedDict):
    Email: str
    CourseTitle: str
    Date: str
    Name: str
    Phone: str
    Batch: str
    BatchID: str
    CertID: str


AWARDEES: AwardeesDict = {
    "Email": "email",
    "CourseTitle": "coursetitle",
    "Date": "dateofcompletion",
    "Name": "name",
    "Phone": "phone",
    "Batch": "batch",
    "BatchID": "batchid",
    "CertID": "certid",
}

AWARDEES_ORDER: list[str] = [
    "Email",
    "CourseTitle",
    "Date",
    "Name",
    "Phone",
    "Batch",
    "BatchID",
    "CertID",
]

AWARDEES_BATCH: str = "NCAIR"
AWARDEES_DATE_FMT: str = ""
AWARDEES_EMTPY: str = " "


FORM_DATE_FMT: str = "%m/%d/%Y"
TIMESTAMP_FMT: str = "%b%d_%H%M%S"


# Column Names of Data
SERIAL: str = "S/N"
NAME: str = "Name"
GENDER: str = "Gender"
PHONE: str = "Phone Number"
EMAIL: str = "Email Address"
COHORT: str = "Cohort"
INTERNSHIP: str = "Category Of Internship"
DATE: str = "Date"
DATE_FMT: str = "%d/%m/%Y"
COMPLETION: str = "NYSC/SIWES Completion Month"
COMPLETION_FMT: str = "%Y/%m/%d"
TRAINING: str = "Choose A Training Course"
UNIQUE_COLUMNS: list[str] = [NAME, EMAIL, PHONE]
TIME: str = "Timestamp"
TIME_FMT: str = "%Y-%m-%d %H:%M:%S"


REGISTRATION_COLS: list[str] = [NAME, EMAIL, PHONE, "Nysc", GENDER, INTERNSHIP]


DATA_COLUMNS: list[str] = [
    SERIAL,
    TIME,
    NAME,
    GENDER,
    COHORT,
    PHONE,
    EMAIL,
    DATE,
    INTERNSHIP,
    COMPLETION,
    TRAINING,
]

# Missing String
NA: str = "N/A"

# NA Columns Replacement
NA_COLUMNS_FILL: dict[str, object] = {
    TIME: datetime.strptime(f"01/01/{datetime.now().year}", DATE_FMT),
    EMAIL: NA,
    PHONE: NA,
    GENDER: NA,
    INTERNSHIP: NA,
    COMPLETION: f"{datetime.now().year}/01/01",
    TRAINING: "Python Beginners (Monday - Wednesday 12:00pm)",
}

# Delimiters / Separators
COMMA: str = ","
COMMA_DELIM: str = ", "
SPACE_DELIM: str = " "
SEMI: str = ";"
SEMI_DELIM: str = "; "
FRONT_SLASH: str = "/"
BACK_SLASH: str = "\\"
HYPHEN: str = "-"

# Column Names for Cache CSV
CACHE_TIME: str = "Timestamp"
CACHE_CMD: str = "Command"
CACHE_ID: str = "Snapshot"


# Column Names for Grading and Collating
SCORE: str = "Score"
GROUP: str = "Group"
ASSESSMENT: str = "Assessment"
ATTENDANCE: str = "Attendance"
REQ: str = "Req"
PROJECT: str = "Project"
RESULT: str = "Result"
COURSE: str = "Course"
COURSE_NAME: str = "Python Beginners"
FROM: str = "FROM"
TO: str = "TO"
DATASTORE: str = "Datastore"
MISSING_NAMES: list[str] = ["Nil", "Null", "None", "N/A"]
CDS: str = "CDS Days"

# Days of the Week
DAYS_IN_WEEK: list[str] = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
]

WEEK_DAY_FMT: str = "%A"


############################################################################
DROPPED_COLUMNS: list[str] = ["Training Days And Hours", "Select Your Batch"]
NAMES_COLUMNS: list[str] = ["First Name", "Last Name", "Middle Name"]
PASSED: str = "Passed"
STATE: str = "State"
PASS: str = "PASS"
FAIL: str = "FAIL"

PLACEHOLDER: str = " "
RESPONSES_NAME: str = "Name"
RESPONSES_NYSC_SIWES: str = "NYSC/SIWES"
RESPONSES_CDS: str = "CDS Days"
RESPONSES_FIRST_NAME: str = "First Name"
RESPONSES_LAST_NAME: str = "Last Name"
RESPONSES_MIDDLE_NAME: str = "Middle Name"
LOG_PATH: str = "./logs"
