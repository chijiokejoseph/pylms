# pylms

A console based learning management system. It includes features such as preprocessing student data from spreadsheets, marking student attendance using forms generated using GCP, and so much more. It is a fledgling project.

___
## Run
To run, use the following commands

1. install the package manager uv
```bash
pip install uv
```

2. create an empty virtual environment
```bash
uv venv
```

3. sync and update dependencies to the virtual environment from the pyproject.toml file
```bash
uv sync
```

4. activate your virtual environment
```bash
source .venv/Scripts/activate # for linux
```
```powershell
.venv\Scripts\activate.ps1 # for powershell
```
```bash
.venv\Scripts\activate # for commmand prompt
```

5. Run the application
```bash
uv run main.py
```

___
## Type Check Project

- Activate the virtual environment
- Run the command below

```bash
basedpyright --outputjson > data/typing.json
```

___
## View Project Dependencies

- Activate the virtual environment
- Run the command below

```bash
pydeps --show-cycles --cluster --max-module-depth 2 -o data/pylms.pdf -T pdf src/pylms
```

___
## DESCRIPTION
PyLMS is a comprehensive console-based learning management system designed for
educational institutions and training programs. The system streamlines the
administration of student cohorts, providing robust tools for managing student
data, tracking attendance, conducting assessments, and generating performance
reports. Built with Python, PyLMS offers a modular architecture that enables
efficient data preprocessing from spreadsheets, automated form generation via
Google Cloud Platform APIs, and systematic tracking of student progress
throughout training programs.

The system maintains persistent state management, allowing administrators to
configure course-specific settings and manage multiple cohorts across different
training courses including Python, Data Science, Product Design, Product
Development, and Embedded Systems. PyLMS features an intelligent error-handling
framework, transaction-based caching with rollback capabilities, and
comprehensive historical tracking of all administrative operations.


KEY FEATURE
-----------
The standout capability of PyLMS is its seamless integration of automated
Google Forms generation with transaction-safe data management. The system
dynamically creates attendance and assessment forms via Google Cloud APIs,
automatically retrieves responses, and processes them into a locally managed
datastore - all while maintaining a command-caching and rollback system that
allows administrators to safely undo operations. This unique combination
eliminates the manual overhead of form creation and data entry while providing
a safety net rarely found in educational software, creating a bridge between
cloud-based data collection and robust local record management with full audit
trail capabilities.

___
FEATURES
--------
1. Student Data Management
   - Automated preprocessing and validation of student registration data from
     Excel spreadsheets
   - Data normalization and cleaning pipelines with duplicate detection
   - Persistent datastore for student records with email, phone, and cohort
     information
   - Support for multiple student categories (NYSC/SIWES internship programs)

2. Attendance Tracking System
   - Interactive attendance recording with present/absent/excused status tracking
   - Date-based class session management with weekday validation
   - CDS (Community Development Service) day tracking for NYSC participants
   - Historical attendance records with timestamp logging
   - Edit capabilities for correcting attendance records

3. Google Forms Integration
   - Automated generation of attendance forms using Google Forms API
   - Dynamic form creation for class sessions, CDS tracking, and student updates
   - API-based form response retrieval and processing
   - Support for assessment and unregistered student forms

4. Learning Management & Assessment
   - Comprehensive grading system for assessments, projects, and attendance
   - Result collation with automated score computation
   - Student performance tracking with pass/fail determination
   - Awardees list generation with certificate ID management
   - Merit-based and fast-track program recognition

5. Communication System
   - Integrated email functionality for sending messages to students
   - Batch email operations with student selection capabilities
   - HTML email template support

6. Transaction Management
   - Command caching with snapshot creation for data recovery
   - Rollback functionality to restore previous system states
   - History tracking for all operations with detailed logging
   - Timestamp-based operation audit trail

7. Configuration Management
   - Course-specific configuration with persistent state storage
   - Data directory management and path validation
   - Open/closed cohort status management
   - Environment variable support for sensitive credentials

8. Interactive CLI Interface
   - Menu-driven navigation system
   - Custom input handlers with validation and quit options
   - Student and date selection interfaces
   - Option-based interactions with user-friendly prompts

___
TECH STACK
----------
Core Language:
- Python 3.12+ (with type hints and modern syntax features)

Data Processing:
- Pandas - DataFrame manipulation and spreadsheet processing
- NumPy - Numerical operations and data validation
- OpenPyXL - Excel file reading and writing

Google Cloud Integration:
- google-api-python-client - Google Forms API interactions
- google-auth-httplib2 - HTTP authentication
- google-auth-oauthlib - OAuth 2.0 authentication flows
- oauth2client - Legacy OAuth support

Configuration & Serialization:
- TOML Kit - Configuration file parsing (state.toml)
- Python-dotenv - Environment variable management
- Pydantic - Data validation and settings management

Development & Testing:
- Pytest - Unit and integration testing framework
- Basedpyright - Type Checking analysis
- Jupyter/Notebook - Interactive development and data analysis

Data Visualization:
- Matplotlib - Charts and statistical visualizations

Additional Libraries:
- python-dateutil - Advanced date parsing and manipulation
- Streamlit - Web-based UI components (future integration)
- pydeps - Dependency analysis

Project Management:
- UV - Modern Python package management and virtual environment handling

Architecture:
- Modular package structure with 17 distinct functional modules
- Approximately 14,000+ lines of Python code
- Type-safe implementation with comprehensive type annotations
- Error handling with custom Result/Error monadic patterns
- Separation of concerns: CLI, data operations, business logic, and API
  integration

___
PROJECT STRUCTURE
-----------------
pylms/
- ├── main.py                # Main application entry point
- ├── src/pylms/
- │   ├── cache/             # Transaction caching and rollback system
- │   ├── clean/             # Transaction caching and rollback system
- │   ├── cli/               # Command-line interface components
- │   ├── cli_utils/         # Command-line interface utilities
- │   ├── config/            # Configuration management
- │   ├── data/              # Data read function and model classes
- │   ├── data_service/      # Data loading, viewing, and operations
- │   ├── email/             # Email sending functionality
- │   ├── form_request/      # API for generating specific forms through GCP
- │   ├── form_retrieve/     # API for retrieving generated form data 
- │   ├── form_utils/        # Utilities for building Form content 
- │   ├── history/           # Operation history tracking
- │   ├── html/              # HTML template generation
- │   ├── lms/               # Core learning management features
- │   ├── messages/          # Message handling system
- │   ├── models/            # Data models and schemas
- │   ├── paths/             # Path management for almost all project data
- │   ├── paths_class/       # Path management for class metadata
- │   ├── preprocess/        # Data preprocessing pipelines
- │   ├── re_phone/          # Phone preprocessing pipelines
- │   ├── result_collate/    # Result collation recording system
- │   ├── result_edit/       # Result update and overwrite system
- │   ├── result_utils/      # Utilities for managing results
- │   ├── rollcall/          # Attendance recording system
- │   ├── rollcall_edit/     # Attendance edit (post-record) system
- │   ├── routines/          # Main workflow routines
- │   ├── service/           # Google Forms Wrapper to simplify functionality
- │   ├── ui/                # User interface components
- │   ├── constants.py/      # Constants and reusables
- │   ├── errors.py/         # Error Handling System
- │   ├── info.py/           # Special Prints (Display) System
- │   ├── mainloop.py/       # Main project loops for Open/Closed cohorts
- │   └── record.py/         # RecordStatus class file
- ├── tests/                 # Integrated tests
- ├── LICENSE                # MIT License
- ├── pyproject.toml         # Project dependencies and metadata
- ├── pyrightconfig.json     # Basedpyright configuration
- └── Readme.md              # Project Overview
