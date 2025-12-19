from datetime import datetime
from pathlib import Path
from typing import Callable, TypedDict

import pandas as pd

PARENT_PATH: Path = Path(__file__).resolve().parents[2]
ENV_PATH: Path = PARENT_PATH / ".env"
DEFAULT_DATA_PATH: Path = PARENT_PATH / "data"
STATE_PATH: Path = DEFAULT_DATA_PATH / "state.toml"
SECRETS_PATH: Path = PARENT_PATH / "secrets.json"
HISTORY_PATH: Path = DEFAULT_DATA_PATH / "history.json"
HISTORY_JSON: str = "history.json"
# RollCall Global Data
GLOBAL_RECORD_PATH: Path = DEFAULT_DATA_PATH / "global_record.json"
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
COMMA = ","
COMMA_DELIM = ", "
SPACE_DELIM = " "
SEMI = ";"
SEMI_DELIM = "; "
FRONT_SLASH = "/"
BACK_SLASH = "\\"
HYPHEN = "-"

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
PROJECT_PENALTY: str = "Project Penalty"
REMARK: str = "Remark"
REASON: str = "Reason"
COURSE: str = "Course"
COURSE_NAME: str = "Python Beginners"
FROM: str = "FROM"
TO: str = "TO"
DATASTORE: str = "Datastore"
MISSING_NAMES: list[str] = ["Nil", "Null", "None", "N/A"]
CDS: str = "CDS Days"

# Days of the Week
WORK_DAYS: list[str] = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
]
WEEK_DAYS: list[str] = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

COURSES: list[str] = [
    "Python Beginners",
    "Python Advanced",
    "Data Science Beginners",
    "Data Science Advanced",
    "Product Design Beginners",
    "Product Design Advanced",
    "Product Development",
    "Embedded Systems",
]

PROGRAM = "Program"

PROGRAMS: list[str] = [
    "NYSC",
    "1 MONTH SIWES",
    "2 MONTHS SIWES",
    "3 MONTHS SIWES",
    "4 MONTHS SIWES",
    "5 MONTHS SIWES",
    "6 MONTHS SIWES",
]

ISSUE = "Issue"

ISSUES: list[str] = [
    "I missed registration",
    "I registered late",
    "I registered for the wrong course",
    "I want to register for Embedded Systems",
    "I was supposed to register for two courses, but I registered one",
    "I registered for the wrong course, I registered late",
    "None of this best describes my issue",
]
EXPLANATION = "Explain Your Issue"
EXPLANATION_STMT = "Write a detailed explanation of your issue"
EVIDENCE = "Attach evidence if applicable"
COURSES_COMPLETE = "Courses Completed"
COURSES_COMPLETE_STMT = "Select the Courses you have completed"
CONFIRM_REG = "Registered"
CONFIRM_REG_STMT = "Did you register before 5pm on Orientation Day"
COURSES_REGISTERED = "Select the course(s) you registered for"


WEEK_DAY_FMT: str = "%A"
MONTH_STR_FMT: str = "%B"


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
