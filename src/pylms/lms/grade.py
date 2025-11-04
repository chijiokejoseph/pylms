from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd

from pylms.constants import GROUP, NAME, SERIAL
from pylms.errors import Result, Unit
from pylms.utils import DataStream, paths, read_data


def prepare_grading(num_groups: int) -> Result[Unit]:
    path: Path = paths.get_group_path()
    if not path.exists():
        return Result[Unit].err(FileNotFoundError(f"path: {path} does not exist."))

    group_data = read_data(path)
    groups_arr = group_data[GROUP].to_numpy()
    for grp_num in range(1, num_groups + 1):
        mask: np.ndarray = cast(np.ndarray, groups_arr == grp_num)
        grp_num_data: pd.DataFrame = group_data.loc[mask, :]
        placeholder: list[str] = ["" for _ in range(grp_num_data.shape[0])]
        grp_grade_data: pd.DataFrame = pd.DataFrame(
            data={
                SERIAL: grp_num_data[SERIAL],
                NAME: grp_num_data[NAME],
                GROUP: grp_num_data[GROUP],
                "Present": placeholder,
                "Active": placeholder,
                "Bonus (5mks)": placeholder,
                "Penalty (10mks)": placeholder,
            }
        )

        grp_grade_stream: DataStream[pd.DataFrame] = DataStream(grp_grade_data)
        grp_grade_path: Path = paths.get_grade_path(grp_num)
        grp_grade_stream.to_excel(grp_grade_path)

    common = {
        SERIAL: [i + 1 for i in range(num_groups)],
        GROUP: [i + 1 for i in range(num_groups)],
    }
    placeholder = ["" for _ in range(num_groups)]
    code_df: pd.DataFrame = pd.DataFrame(
        data={
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

    grading_path: Path = paths.get_grade_path()

    presentation_df: pd.DataFrame = pd.DataFrame(
        data={
            **common,
            "Presentation Score (100mks)": placeholder,
            "Question (Presenters) -10mks": placeholder,
            "Question (Leaders) -15mks": placeholder,
            "Question1 (Rest) -10mks": placeholder,
            "Question2 (Rest) -10mks": placeholder,
            "Total (100mks)": placeholder,
        }
    )

    total_df: pd.DataFrame = pd.DataFrame(
        data={
            **common,
            "Code (100mks)": placeholder,
            "Presentation (100mks)": placeholder,
            "Total (100mks)": placeholder,
        }
    )

    with pd.ExcelWriter(grading_path) as file:
        code_df.to_excel(file, index=False, sheet_name="Code")  # pyright: ignore[reportUnknownMemberType]
        presentation_df.to_excel(file, index=False, sheet_name="Presentation")  # pyright: ignore[reportUnknownMemberType]
        total_df.to_excel(file, index=False, sheet_name="Total")  # pyright: ignore[reportUnknownMemberType]

    return Result[Unit].unit()
