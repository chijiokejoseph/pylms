import re
from email.message import EmailMessage
from smtplib import SMTP

from ..cli import input_bool
from ..config import Config, read_course_name
from ..constants import COHORT, COMMA_DELIM, EMAIL, GENDER, NAME, REASON, REMARK
from ..data import DataStore, DataStream, read
from ..email import MailError, run_email
from ..errors import LMSError, Result, Unit, eprint
from ..info import print_info
from ..paths import get_paths_excel
from .find import find_col

type MailResultError = tuple[int, str, str, MailError]


def _send_result(config: Config, ds: DataStore, server: SMTP) -> Result[Unit]:
    """Send individualized result breakdown emails to students.

    Reads result data from Excel file, extracts relevant columns for each student,
    formats personalized messages with scores and requirements, and sends emails.

    Args:
        config (Config): Configuration object containing email settings.
        ds (DataStore): DataStore instance containing student data.
        server (SMTP): SMTP server instance for sending emails.

    Returns:
        Result[Unit]: Success or error with message.
    """
    # Get sender email and course info
    sender_email = config.admin

    # format the facilitator names to be included in the message
    names = [f.name.title() for f in config.facilitators]
    first  = names[:-1]
    last = names[-1]
    names_print = COMMA_DELIM.join(first)
    names_print = f"{names_print} and {last}"

    path = get_paths_excel(config)["Result"]

    course_name = read_course_name(config)
    if course_name.is_err():
        return course_name.propagate()
    course_name = course_name.unwrap()

    # Read result data
    result = read(path)
    if result.is_err():
        return result.propagate()
    result = result.unwrap()

    result_stream = DataStream(result)
    data = ds.as_ref()

    # Find column names
    assessment_score_col = find_col(result_stream, "Assessment", "Score").unwrap()
    assessment_max_match = re.search(r"(\d+)", assessment_score_col)
    if assessment_max_match is None:
        msg = "Error parsing assessment max score"
        eprint(f"{msg}\n")
        return Result.err(msg)
    assessment_max = float(assessment_max_match.group(1))

    assessment_req_col = find_col(result_stream, "Assessment", "Req").unwrap()
    attendance_count_col = find_col(result_stream, "Attendance", "Count").unwrap()
    attendance_score_col = find_col(result_stream, "Attendance", "Score").unwrap()
    attendance_req_col = find_col(result_stream, "Attendance", "Req").unwrap()
    project_score_col = find_col(result_stream, "Project", "Score").unwrap()

    project_max_match = re.search(r"(\d+)", project_score_col)
    if project_max_match is None:
        msg = "Error parsing project max score"
        print(f"{msg}\n")
        return Result.err(msg)
    project_max = float(project_max_match.group(1))

    result_col = find_col(result_stream, "Result", "Score").unwrap()
    result_req_col = find_col(result_stream, "Result", "Req").unwrap()

    # Extract requirements
    assessment_req = result[0, assessment_req_col]
    attendance_req = result[0, attendance_req_col]
    result_req = result[0, result_req_col]

    # Calculate total classes
    attendance_count_data = result[attendance_count_col]
    attendance_score_data = result[attendance_score_col]
    classes_calc = 100 * attendance_count_data / attendance_score_data
    classes = int(round(classes_calc.mode().item(), 0))

    bad_records: list[MailResultError] = []

    # Process each student
    for idx in range(result.height):
        # Extract scores for current student
        assessment_score = result[idx, assessment_score_col]
        attendance_count = result[idx, attendance_count_col]
        attendance_score = result[idx, attendance_score_col]
        project_score = result[idx, project_score_col]
        result_score = result[idx, result_col]
        remark = result[idx, REMARK].strip()
        reason = result[idx, REASON].strip()

        marks = result_score - (assessment_score + project_score)
        marks = round(marks, 0)

        if marks < 0:
            penalty_marks = -1 * int(marks)
            bonus_marks = 0
        else:
            penalty_marks = 0
            bonus_marks = int(marks)

        # Extract student info
        name = result[idx, NAME].strip()
        gender = data[idx, GENDER].strip()
        email = data[idx, EMAIL].strip()

        if email == "":
            bad_records.append(
                (idx + 1, name, email, {"error": (1, b"Email is empty")})
            )
            continue

        cohort = data[idx, COHORT]

        # Format score strings
        attendance_score_str = f"{attendance_score:.2f}%"
        attendance_req_str = f"{attendance_req:.0f}%"
        assessment_score_str = f"{assessment_score:.2f}%"
        assessment_req_str = f"{assessment_req:.2f}%"
        project_score_str = f"{project_score:.2f}%"
        result_score_str = f"{result_score:.2f}%"
        result_req_str = f"{result_req:.0f}%"
        bonus_marks_str = f"{bonus_marks:.0f}%"
        penalty_marks_str = f"{penalty_marks:.0f}%"

        # Compose personalized message
        msg = f"""
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
  <p>{names_print}</p>
</footer>
        """

        # Create email message
        email_msg = EmailMessage()
        email_msg["Subject"] = f"{course_name} Cohort {cohort} Result"
        email_msg.set_content(
            "This is an HTML email. Please view in a compatible client."
        )
        email_msg.add_alternative(msg, subtype="html")

        try:
            # Send test email to facilitators first
            if idx == 0:
                email_msg = EmailMessage()
                email_msg["Subject"] = f"Test: {course_name} Cohort {cohort} Result"
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
                gmails = [f.gmail for f in config.facilitators]
                gmails_print = COMMA_DELIM.join(gmails)
                send_err = server.send_message(
                    email_msg, from_addr=sender_email, to_addrs=gmails
                )

                confirm = input_bool(
                    prompt=f"Please confirm the format of the email as sent to any of {gmails_print}. Is it okay? ",
                )
                if confirm.is_err():
                    return confirm.propagate()
                confirm = confirm.unwrap()
                if not confirm:
                    return Result.err(Exception("Email format not okay"))

            send_err = server.send_message(
                email_msg, from_addr=sender_email, to_addrs=email
            )
        except Exception as e:
            send_err = {"error": (1, bytes(str(e), "utf-8"))}

        num = idx + 1
        if send_err != {}:
            bad_records.append((num, name, email, send_err))
        else:
            print_info(
                f"S/N: {num}. Successfully sent email to {name} with email: {email}"
            )

    # Report any errors
    for num, name, email, send_err in bad_records:
        eprint(
            f"\nS/N: {num}. Error sending email to {name} with email: {email}.\nError encountered: {send_err}"
        )

    if len(bad_records) > 0:
        err = LMSError(f"Failed to send emails to {len(bad_records)} recipients.")
        return Result.err(err)

    return Result.unit()


def mail_result(config: Config, ds: DataStore) -> Result[Unit]:
    """Initiate process of sending result emails to students.

    Delegates email sending to utility that manages SMTP connection
    and ensures each student receives individualized result email.

    Args:
        config (Config): Configuration object containing email settings.
        ds (DataStore): DataStore instance containing student data.

    Returns:
        Result[Unit]: Success or error from email sending process.
    """
    return run_email(config, lambda server: _send_result(config, ds, server))
