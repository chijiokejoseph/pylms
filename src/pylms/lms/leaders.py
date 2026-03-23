import random
import re
from pathlib import Path
from typing import Literal, NamedTuple

import polars as pl

from ..config import Config
from ..constants import GENDER, GROUP, NAME, SERIAL
from ..data import DataStore, read, write
from ..errors import Result, Unit, eprint
from ..history import History, get_num_groups
from ..paths import (
    get_criterion_path,
    get_grading_leader,
    get_group_criterion_path,
    get_group_path,
    get_leader_path,
)


class Nominations(NamedTuple):
    present_counts: list[int]
    nominees: list[int]


class LeaderMap(NamedTuple):
    leader: int
    assistant: int
    leaders: list[int]
    assistants: list[int]


def get_present_count(ds: DataStore, serial: int) -> int:
    data = ds.as_ref()
    columns: list[str] = data.columns
    date_columns: list[str] = [
        col for col in columns if re.match(r"\d{2}/\d{2}/\d{4}", col) is not None
    ]
    row = data.select(pl.col(date_columns)).row(serial - 1)
    return sum(
        1 for entry in row if isinstance(entry, str) and entry.lower() == "present"
    )


def absent_expr(col: str) -> pl.Expr:
    return (pl.col(col) == "Absent") | (pl.col(col).str.strip_chars() == "")


def get_nominations(
    ds: DataStore, serials: list[int], gender_type: Literal["Male", "Female"]
) -> Nominations:
    data = ds.as_ref()
    columns: list[str] = data.columns
    date_columns: list[str] = [
        col for col in columns if re.match(r"\d{2}/\d{2}/\d{4}", col) is not None
    ]

    present = (
        data.select(pl.col(date_columns))
        .with_columns(
            [
                pl.when(absent_expr(col))
                .then(pl.lit(0))
                .otherwise(pl.lit(1))
                .alias(col)
                for col in date_columns
            ]
        )
        .sum_horizontal()
    )
    genders = (
        data.select(pl.col(GENDER, SERIAL))
        .with_columns(pl.Series("Count", present).alias("Count"))
        .filter(pl.col(SERIAL).is_in(serials))
        .filter(pl.col(GENDER) == gender_type)
    )

    # @np.vectorize
    # def get_gender_serials(serial: int):
    #     return get_present_count(ds, serial)

    # present = datamap(
    #     genders, SERIAL, get_gender_serials, np.int64, pl.Int64(), new_col="Count"
    # )

    max_count: int = genders.select(pl.col("Count").max()).item()

    nominees: list[int] = genders.filter(pl.col("Count") == max_count)[SERIAL].to_list()
    present_counts: list[int] = genders["Count"].to_list()

    return Nominations(present_counts=present_counts, nominees=nominees)


def choose_leader(
    male_nominations: Nominations, female_nominations: Nominations, group: int
) -> LeaderMap:
    male_nominees = male_nominations.nominees
    female_nominees = female_nominations.nominees
    if group % 2 == 0:
        leader: int = random.choice(male_nominees)
        leaders: list[int] = male_nominees
        assistant: int = (
            random.choice(female_nominees)
            if len(female_nominees) > 0
            else random.choice(male_nominees)
        )
        assistants: list[int] = (
            female_nominees if len(female_nominees) > 0 else male_nominees
        )
    else:
        leader = (
            random.choice(female_nominees)
            if len(female_nominees) > 0
            else random.choice(male_nominees)
        )
        leaders = female_nominees if len(female_nominees) > 0 else male_nominees
        assistant = random.choice(male_nominees)
        assistants = male_nominees

    return LeaderMap(leader, assistant, leaders, assistants)


def select_leaders(config: Config, ds: DataStore, history: History) -> Result[Unit]:
    if not history.has_group:
        msg = "Students have not been grouped yet."
        eprint(msg)
        return Result.err(msg)

    data = ds.as_ref()

    groups = get_num_groups(history)
    leader_serials: list[int] = []
    assistant_serials: list[int] = []
    leader_names: list[str] = []
    assistant_names: list[str] = []
    leader_groups: list[int] = []

    for group in range(1, groups + 1):
        group_path: Path = get_group_path(config, group)
        if not group_path.exists():
            msg = f"Group file for group {group} does not exist."
            eprint(msg)
            return Result.err(msg)

        group_df = read(group_path)

        if group_df.is_err():
            return group_df.propagate()

        group_df = group_df.unwrap()

        serials: list[int] = group_df[SERIAL].to_list()

        genders: list[str] = (
            group_df.join(data.select([SERIAL, GENDER]), on=SERIAL, how="inner")
            .select(GENDER)
            .to_series()
            .to_list()
        )

        male_nominations: Nominations = get_nominations(ds, serials, "Male")
        female_nominations: Nominations = get_nominations(ds, serials, "Female")

        leader, assistant, leaders, assistants = choose_leader(
            male_nominations, female_nominations, group
        )
        leader_name: str = (
            group_df.filter(pl.col(SERIAL) == leader).select(pl.col(NAME)).item()
        )

        present_counts: list[int] = [
            get_present_count(ds, serial) for serial in serials
        ]
        assistant_name: str = (
            group_df.filter(pl.col(SERIAL) == assistant).select(pl.col(NAME)).item()
        )

        leader_serials.append(leader)
        leader_names.append(leader_name)
        leader_groups.append(group)

        assistant_serials.append(assistant)
        assistant_names.append(assistant_name)

        group_df = (
            group_df.lazy()
            .with_columns(
                pl.Series("Count", present_counts),
                pl.Series(GENDER, genders),
                pl.Series(
                    "Potential Leader",
                    ["True" if serial in leaders else "False" for serial in serials],
                ),
                pl.Series(
                    "Potential Assistant Leader",
                    ["True" if serial in assistants else "False" for serial in serials],
                ),
                pl.Series(
                    "Leader",
                    ["Leader" if serial == leader else "" for serial in serials],
                ),
                pl.Series(
                    "Assistant",
                    [
                        "Assistant Leader" if serial == assistant else ""
                        for serial in serials
                    ],
                ),
            )
            .collect()
        )
        criterion_path = get_criterion_path(config)
        criterion_path.mkdir(exist_ok=True)
        group_criterion_path = get_group_criterion_path(config, group)
        result = write(group_df, group_criterion_path)
        if result.is_err():
            return result.propagate()

    leaders = pl.DataFrame(
        data={SERIAL: leader_serials, "Leader Name": leader_names, GROUP: leader_groups}
    )

    assistants = pl.DataFrame(
        data={
            SERIAL: assistant_serials,
            "Assistant Leader Name": assistant_names,
            GROUP: leader_groups,
        }
    )

    result = write(leaders, get_leader_path(config, "Leader"))
    if result.is_err():
        return result.propagate()

    result = write(leaders, get_grading_leader(config, "Leader"))
    if result.is_err():
        return result.propagate()

    result = write(assistants, get_leader_path(config, "Assistant"))
    if result.is_err():
        return result.propagate()

    result = write(assistants, get_grading_leader(config, "Assistant"))
    if result.is_err():
        return result.propagate()

    return Result.unit()
