from pathlib import Path

import polars as pl

from ..constants import GROUP, SERIAL
from ..data import read, write
from ..errors import Result, Unit, eprint
from ..paths import get_grade_path, get_group_dir, get_group_path


def prepare_grading(num_groups: int) -> Result[Unit]:
    """Prepare grading spreadsheets for project evaluation.

    Creates individual group grading sheets and summary grading workbooks
    for code evaluation, presentation scoring, and total calculations.

    Args:
        num_groups (int): Number of project groups to create sheets for.

    Returns:
        Result[Unit]: Success or error with message.
    """
    path = get_group_path()
    if not path.exists():
        msg = f"path: {path} does not exist."
        eprint(msg)
        return Result.err(msg)

    group = read(path)
    if group.is_err():
        return group.propagate()
    group = group.unwrap()

    # Create individual group grading sheets
    for num in range(1, num_groups + 1):
        # Filter data for current group
        grade_num = group.filter(pl.col(GROUP) == num).with_columns(
            [
                pl.lit("").alias("Present"),
                pl.lit("").alias("Active"),
                pl.lit("").alias("Bonus (5mks)"),
                pl.lit("").alias("Penalty (10mks)"),
            ]
        )

        grade_path = get_grade_path(num)
        result = write(grade_num, grade_path)
        if result.is_err():
            return result.propagate()

    # Create summary grading workbooks
    common = {
        SERIAL: list(range(1, num_groups + 1)),
        GROUP: list(range(1, num_groups + 1)),
    }
    placeholder = ["" for _ in range(num_groups)]

    code_df = pl.DataFrame(
        {
            **common,
            "Documentation (15mks)": placeholder,
            "Naming (10mks)": placeholder,
            "Code Correctness (15mks)": placeholder,
            "Readability (15mks)": placeholder,
            "Modularization (15mks)": placeholder,
            "Functionality (15mks)": placeholder,
            "UX (15mks)": placeholder,
            "Total (100mks)": placeholder,
        }
    )

    presentation_df = pl.DataFrame(
        {
            **common,
            "Presentation Score (100mks)": placeholder,
            "Question (Presenters) -10mks": placeholder,
            "Question (Leaders) -15mks": placeholder,
            "Question1 (Rest) -10mks": placeholder,
            "Question2 (Rest) -10mks": placeholder,
            "Total (100mks)": placeholder,
        }
    )

    total_df = pl.DataFrame(
        {
            **common,
            "Code (100mks)": placeholder,
            "Presentation (100mks)": placeholder,
            "Total (100mks)": placeholder,
        }
    )

    grading_path = get_grade_path()
    group_path = get_group_dir() / grading_path.name

    # Write multi-sheet workbooks
    result = write_sheets(
        grading_path,
        (code_df, "Code"),
        (presentation_df, "Presentation"),
        (total_df, "Total"),
    )
    if result.is_err():
        return result.propagate()

    result = write_sheets(
        group_path,
        (code_df, "Code"),
        (presentation_df, "Presentation"),
        (total_df, "Total"),
    )
    if result.is_err():
        return result.propagate()

    return Result.unit()


def write_sheets(path: Path, *dfs: tuple[pl.DataFrame, str]) -> Result[Unit]:
    """Write multiple DataFrames to Excel workbook with separate sheets.

    Args:
        path (Path): Output Excel file path.
        *dfs: Tuples of (DataFrame, sheet_name) to write.

    Returns:
        Result[Unit]: Success or error with message.
    """
    for df, sheet in dfs:
        result = write(df, path, worksheet=sheet)
        if result.is_err():
            return result.propagate()

    return Result.unit()
