from pathlib import Path
from pylms.cli.option_input import input_option
from pylms.utils import paths, read_data, DataStream, DataStore, must_get_env
from pylms.config import read_course_name
from pylms.lms.utils import find_col
from pylms.constants import REASON, REMARK, NAME, GENDER, EMAIL, COHORT
import pandas as pd
import re
from smtplib import SMTP
from email.message import EmailMessage
from pylms.email import run_email
from pylms.errors import LMSError, Result, Unit


def _send_result(ds: DataStore, server: SMTP) -> Result[Unit]:
    """
    Sends individualized result breakdown emails to students using the provided SMTP server.

    Reads result data from an Excel file, extracts relevant columns for each student,
    formats a personalized message with their scores and requirements, and sends the message
    to the student's email address.

    :param ds: (DataStore) - A DataStore instance containing student data.
    :type ds: DataStore
    :param server: (SMTP) - An SMTP server instance used to send emails.
    :type server: SMTP

    :return: (Result[Unit]) - returns a Result object indicating success or failure.
    :rtype: Result[Unit]

    :raises Exception: Any exceptions raised by the SMTP server's send_message method or data reading functions will propagate.
    """

    # Get the sender's email address from environment variables
    sender_email: str = must_get_env("EMAIL")

    # Get the path to the result Excel file
    path: Path = paths.get_paths_excel()["Result"]

    # Read the result data into a DataFrame
    result: pd.DataFrame = read_data(path)

    # Wrap the DataFrame in a DataStream for further processing
    result_stream: DataStream[pd.DataFrame] = DataStream(result)
    result = result_stream()

    # Get the data from the DataStore
    data: pd.DataFrame = ds.as_ref()

    # Find the relevant column names for each required field
    assessment_score_col: str = find_col(result_stream, "Assessment", "Score")
    assessment_max_match: re.Match[str] | None = re.search(
        r"(\d+)", assessment_score_col
    )
    if assessment_max_match is None:
        err_msg: str = "Error parsing assessment max score"
        print(f"\n{err_msg}\n")
        return Result[Unit].err(Exception(err_msg))
    assessment_max: float = float(assessment_max_match.group(1))

    assessment_req_col: str = find_col(result_stream, "Assessment", "Req")

    attendance_count_col: str = find_col(result_stream, "Attendance", "Count")
    attendance_score_col: str = find_col(result_stream, "Attendance", "Score")
    attendance_req_col: str = find_col(result_stream, "Attendance", "Req")

    project_score_col: str = find_col(result_stream, "Project", "Score")
    project_max_match: re.Match[str] | None = re.search(r"(\d+)", project_score_col)
    if project_max_match is None:
        err_msg = "Error parsing project max score"
        print(f"\n{err_msg}\n")
        return Result[Unit].err(Exception(err_msg))
    project_max: float = float(project_max_match.group(1))

    result_col: str = find_col(result_stream, "Result", "Score")
    result_req_col: str = find_col(result_stream, "Result", "Req")

    # extract all requirements
    assessment_req: float = result.loc[:, assessment_req_col].astype(float).iloc[0]
    attendance_req: float = result.loc[:, attendance_req_col].astype(float).iloc[0]
    result_req: float = result.loc[:, result_req_col].astype(float).iloc[0]

    attendance_score_data: pd.Series = (
        100
        * result.loc[:, attendance_count_col]
        / result.loc[:, attendance_score_col].astype(float)
    )
    classes_float: float = attendance_score_data.mode().iloc[0]
    classes: int = int(round(classes_float, 0))

    bad_records: list[tuple[int, str, str, dict]] = []

    # Iterate over each student in the result DataFrame
    for idx in range(result.shape[0]):
        # Extract all scores and requirements for the current student
        assessment_score: float = (
            result.loc[:, assessment_score_col].astype(float).iloc[idx]
        )
        attendance_count: int = (
            result.loc[:, attendance_count_col].astype(int).iloc[idx]
        )
        attendance_score: float = (
            result.loc[:, attendance_score_col].astype(float).iloc[idx]
        )

        project_score: float = result.loc[:, project_score_col].astype(float).iloc[idx]
        result_score: float = result.loc[:, result_col].astype(float).iloc[idx]

        remark: str = result.loc[:, REMARK].astype(str).iloc[idx]
        reason: str = result.loc[:, REASON].astype(str).iloc[idx]

        marks: float = result_score - (assessment_score + project_score)
        marks = round(marks, 0)

        if marks < 0:
            penalty_marks: int = -1 * int(marks)
            bonus_marks: int = 0
        else:
            penalty_marks = 0
            bonus_marks = int(marks)

        # Extract data fields for the current student
        name: str = result.loc[:, NAME].astype(str).iloc[idx]
        name = name.strip()
        gender: str = data.loc[:, GENDER].astype(str).iloc[idx]
        gender = gender.strip()
        email: str = data.loc[:, EMAIL].astype(str).iloc[idx]
        email = email.strip()

        # Check if the email is empty
        if email == "":
            bad_records.append((idx + 1, name, email, {"error": (1, "Email is empty")}))
            continue

        cohort: int = data.loc[:, COHORT].astype(int).iloc[idx]

        attendance_score_str: str = f"{attendance_score:.2f}%"
        attendance_req_str: str = f"{attendance_req:.0f}%"
        assessment_score_str: str = f"{assessment_score:.2f}%"
        assessment_req_str: str = f"{assessment_req:.2f}%"
        project_score_str: str = f"{project_score:.2f}%"
        result_score_str: str = f"{result_score:.2f}%"
        result_req_str: str = f"{result_req:.0f}%"
        bonus_marks_str: str = f"{bonus_marks:.0f}%"
        penalty_marks_str: str = f"{penalty_marks:.0f}%"

        # Compose the personalized message for the student
        msg: str = f"""
<h2>
  <bold>
    Dear {"Mr. " if gender.strip().lower().startswith("m") else "Ms. " if gender.strip().lower().startswith("f") else ""}{name},
  <bold>
</h2>

<p>Greetings. The breakdown for your result is as follows:</p>

<p>Attendance: You attended {attendance_count} / {classes} classes.</p>

<table border="1" cellspacing="4" cellpadding="8" style="border-collapse: separate; border-spacing: 8px;">
    <thead>
      <tr>
        <th style="padding: 10px;">Metric</th>
        <th style="padding: 10px;">Score</th>
        <th style="padding: 10px;">Requirement</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px;">Attendance (100%)</td>
        <td style="padding: 8px;">{attendance_score_str}</td>
        <td style="padding: 8px;">{attendance_req_str}</td>
      </tr>
      <tr>
        <td style="padding: 8px;">Assessment ({assessment_max:.0f}%)</td>
        <td style="padding: 8px;">{assessment_score_str}</td>
        <td style="padding: 8px;">{assessment_req_str}</td>
      </tr>
      <tr>
        <td style="padding: 8px;">Project ({project_max:.0f}%)</td>
        <td style="padding: 8px;">{project_score_str}</td>
        <td style="padding: 8px;">N/A</td>
      </tr>
      <tr>
        <td style="padding: 8px;">Bonus Marks (+ve)</td>
        <td style="padding: 8px;">{bonus_marks_str}</td>
        <td style="padding: 8px;">N/A</td>
      </tr>
      <tr>
        <td style="padding: 8px;">Penalty Marks (-ve)</td>
        <td style="padding: 8px;">{penalty_marks_str}</td>
        <td style="padding: 8px;">N/A</td>
      </tr>
      <tr>
        <td style="padding: 8px;">Result (100%)</td>
        <td style="padding: 8px;">{result_score_str}</td>
        <td style="padding: 8px;">{result_req_str}</td>
      </tr>
    </tbody>
</table>    
    
<h2 style="text-align: center;">Result Formula</h2>
    
<p style="text-align: center;">
  <italic>
    RESULT = ASSESSMENT + PROJECT + BONUS MARKS - PENALTY MARKS
  <italic>
</p>
    
<table border="1" cellspacing="4" cellpadding="8" style="border-collapse: separate; border-spacing: 8px;">
    <thead>
      <tr>
        <th style="padding: 10px;">Remark</th>
        <th style="padding: 10px;">Reason</th>
      </tr>
    </thead>
    <tbody>
      <td style="padding: 8px;">{remark}</td>
      <td style="padding: 8px;">{reason}</td>
    </tbody>
</table>
    
<p>I hope this gives you a good understanding of where you stand in your programming journey.</p>

<footer>
  <p>Best regards,</p>
  <p>Jason and Joseph</p>
</footer>
        """

        # Create the email message
        email_msg: EmailMessage = EmailMessage()
        email_msg["Subject"] = f"{read_course_name()} Cohort {cohort} Result"
        email_msg.set_content(
            "This is an HTML email. Please view in a compatible client."
        )
        email_msg.add_alternative(msg, subtype="html")

        try:
            # Send the email to the student
            if idx == 0:
                email_msg = EmailMessage()
                email_msg["Subject"] = (
                    f"Test: {read_course_name()} Cohort {cohort} Result"
                )
                email_msg.set_content(
                    "This is an HTML email. Please view in a compatible client."
                )
                mod_msg = f"""
<h2>
  <bold>
    Dear Facilitator. Please confirm the format for this email before I send to all the students.
  <bold>
</h2>
{msg}
              """
                email_msg.add_alternative(mod_msg, subtype="html")
                email1: str = must_get_env("FACILITATOR_EMAIL1")
                email2: str = must_get_env("FACILITATOR_EMAIL2")
                send_err: dict[str, tuple[int, bytes]] = server.send_message(
                    email_msg, from_addr=sender_email, to_addrs=[email1, email2]
                )
                
                option_result = input_option(
                    ["Yes", "No"],
                    prompt=f"Please confirm the format of the email as sent to either {email1} or {email2}. Is it okay? ",
                )
                if option_result.is_err():
                    return Result[Unit].err(option_result.unwrap_err())
                option_idx, _ = option_result.unwrap()
                if option_idx != 1:
                    return Result[Unit].err(Exception("Email format not okay"))
                  
            send_err = server.send_message(email_msg, from_addr=sender_email, to_addrs=email)
        except Exception as e:
            send_err = {"error": (1, bytes(str(e), "utf-8"))}

        num: int = idx + 1
        if send_err != {}:
            bad_records.append((num, name, email, send_err))
        else:
            print(
                f"\nS/N: {num}. Successfully sent email to {name} with email: {email}"
            )

    for num, name, email, send_err in bad_records:
        print(
            f"\nS/N: {num}. Error sending email to {name} with email: {email}.\nError encountered: {send_err}"
        )
    if len(bad_records) > 0:
        err = LMSError(f"Failed to send emails to {len(bad_records)} recipients.")
        return Result[Unit].err(err)

    return Result[Unit].unit()


def send_result(ds: DataStore) -> None:
    """
    Initiates the process of sending result emails to students.

    This function delegates the email sending process to a utility that is responsible for
    setting up the email environment (such as establishing an SMTP server connection),
    performing the actual email sending logic, and handling any necessary cleanup or error management.

    The function ensures that each student receives an individualized result email with their scores and requirements.

    :param ds: (DataStore) - A DataStore instance containing student data.
    :type ds: DataStore
    :return: (None) - This function does not return a value.
    :rtype: None
    :raises Exception: Any exceptions raised during the email sending process (such as SMTP errors) may propagate.
    """

    # Run the email sending process using the configured email utility.
    # The lambda ensures the DataStore is passed to the result-sending logic.
    run_email(lambda server: _send_result(ds, server))
