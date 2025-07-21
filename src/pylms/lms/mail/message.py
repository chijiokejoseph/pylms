from pathlib import Path
from pylms.utils import paths, read_data, DataStream
from pylms.lms.utils import find_col, det_passmark_col
from pylms.constants import REASON, REMARK, NAME, GENDER, EMAIL
import pandas as pd
from smtplib import SMTP
from pylms.email import run_email


def _send_result(server: SMTP) -> None:
    """
    Sends individualized result breakdown emails to students using the provided SMTP server.

    Reads result data from an Excel file, extracts relevant columns for each student,
    formats a personalized message with their scores and requirements, and sends the message
    to the student's email address.

    :param server: (SMTP) - An SMTP server instance used to send emails.
    :type server: SMTP
    :return: (None) - This function does not return a value.
    :rtype: None
    :raises Exception: Any exceptions raised by the SMTP server's sendmail method or data reading functions will propagate.
    """
    # Get the path to the result Excel file
    path: Path = paths.get_paths_excel()["Result"]

    # Read the result data into a DataFrame
    result: pd.DataFrame = read_data(path)

    # Wrap the DataFrame in a DataStream for further processing
    result_stream: DataStream[pd.DataFrame] = DataStream(result)
    result = result_stream()

    # Find the relevant column names for each required field
    assessment_score_col: str = find_col(result_stream, "Assessment", "Score")
    assessment_req_col: str = find_col(result_stream, "Assessment", "Req")
    attendance_count_col: str = find_col(result_stream, "Attendance", "Count")
    attendance_score_col: str = find_col(result_stream, "Attendance", "Score")
    attendance_req_col: str = find_col(result_stream, "Attendance", "Req")
    project_score_col: str = find_col(result_stream, "Project", "Score")
    result_col: str = find_col(result_stream, "Result", "Score")
    result_req_col: str = find_col(result_stream, "Result", "Req")
    passmark_col: str = det_passmark_col()

    # Iterate over each student in the result DataFrame
    for idx in range(result.shape[0]):
        # Extract and convert all relevant fields for the current student
        assessment_score: float = (
            result.loc[:, assessment_score_col].astype(float).iloc[idx]
        )
        assessment_req: float = (
            result.loc[:, assessment_req_col].astype(float).iloc[idx]
        )
        attendance_count: float = (
            result.loc[:, attendance_count_col].astype(float).iloc[idx]
        )
        attendance_score: float = (
            result.loc[:, attendance_score_col].astype(float).iloc[idx]
        )
        attendance_req: float = (
            result.loc[:, attendance_req_col].astype(float).iloc[idx]
        )
        project_score: float = result.loc[:, project_score_col].astype(float).iloc[idx]
        result_score: float = result.loc[:, result_col].astype(float).iloc[idx]
        result_req: float = result.loc[:, result_req_col].astype(float).iloc[idx]
        passmark: float = result.loc[:, passmark_col].astype(float).iloc[idx]
        remark: str = result.loc[:, REMARK].astype(str).iloc[idx]
        reason: str = result.loc[:, REASON].astype(str).iloc[idx]
        name: str = result.loc[:, NAME].astype(str).iloc[idx]
        gender: str = result.loc[:, GENDER].astype(str).iloc[idx]
        email: str = result.loc[:, EMAIL].astype(str).iloc[idx]

        # Compose the personalized message for the student
        msg: str = f"""
Dear {"Mr. " if gender.strip().lower().startswith("m") else "Ms. " if gender.strip().lower().startswith("f") else ""}{name},

Greetings. The breakdown for your result is as follows:
    Attendance: You attended {attendance_count} classes.
    Attendance Score: {attendance_score}%
    Attendance Requirement: {attendance_req}%
    
    Assessment Score: {assessment_score}%
    Assessment Requirement: {assessment_req}%
    
    Project Score: {project_score}%
    
    Result Score: {result_score}%
    Result Requirement: {result_req}%
    
    Passmark: {passmark}%
    
    Remark: {remark}
    Reason: {reason}
    
I hope this gives you a good understanding of where you stand in your programming journey.

Best regards,
Jason and Joseph
        """

        # Send the email to the student
        server.sendmail("email", email, msg)


def send_result() -> None:
    """
    Initiates the process of sending result emails to students.

    This function delegates the email sending process to a utility that is responsible for
    setting up the email environment (such as establishing an SMTP server connection),
    performing the actual email sending logic, and handling any necessary cleanup or error management.

    The function ensures that each student receives an individualized result email with their scores and requirements.

    :return: (None) - This function does not return a value.
    :rtype: None
    :raises Exception: Any exceptions raised during the email sending process (such as SMTP errors) may propagate.
    """

    # Run the email sending process using the configured email utility
    run_email(_send_result)
