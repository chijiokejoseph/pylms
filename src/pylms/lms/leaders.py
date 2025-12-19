import random
import re
from pathlib import Path
from typing import Literal, NamedTuple

import pandas as pd

from ..constants import GENDER, GROUP, NAME, SERIAL
from ..data import DataStore, DataStream, read
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
    data: pd.DataFrame = ds.as_ref()
    columns: list[str] = data.columns.tolist()
    date_columns: list[str] = [
        col for col in columns if re.match(r"\d{2}/\d{2}/\d{4}", col) is not None
    ]
    data_row = data.loc[:, date_columns].iloc[serial - 1].astype(str)
    return sum(1 for entry in data_row if entry.lower() == "present")


def get_nominations(
    ds: DataStore, serials: list[int], gender_type: Literal["Male", "Female"]
) -> Nominations:
    genders: list[str] = [
        ds.as_ref()[GENDER].astype(str).iloc[serial - 1] for serial in serials
    ]
    gender_serials: list[tuple[Literal["Male", "Female"], int]] = [
        (gender_type, serial)
        for gender, serial in zip(genders, serials)
        if gender == gender_type
    ]

    present_counts: list[int] = [
        get_present_count(ds, serial) for _, serial in gender_serials
    ]

    max_count: int = max(present_counts)

    nominees: list[int] = [
        gender_serials[idx][1]
        for idx, count in enumerate(present_counts)
        if count == max_count
    ]

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


def select_leaders(ds: DataStore, history: History) -> Result[Unit]:
    if not history.has_group:
        msg = "Students have not been grouped yet."
        eprint(msg)
        return Result.err(msg)

    groups = get_num_groups(history)
    leader_serials: list[int] = []
    assistant_serials: list[int] = []
    leader_names: list[str] = []
    assistant_names: list[str] = []
    leader_groups: list[int] = []

    for group in range(1, groups + 1):
        group_path: Path = get_group_path(group)
        if not group_path.exists():
            msg = f"Group file for group {group} does not exist."
            eprint(msg)
            return Result.err(msg)

        group_data = read(group_path)

        if group_data.is_err():
            return group_data.propagate()

        group_data = group_data.unwrap()

        serials: list[int] = group_data[SERIAL].tolist()

        genders: list[str] = [
            ds.as_ref()[GENDER].astype(str).iloc[serial - 1] for serial in serials
        ]

        male_nominations: Nominations = get_nominations(ds, serials, "Male")
        female_nominations: Nominations = get_nominations(ds, serials, "Female")

        leader, assistant, leaders, assistants = choose_leader(
            male_nominations, female_nominations, group
        )

        leader_name: str = (
            group_data.loc[group_data[SERIAL] == leader, NAME].astype(str).iloc[0]
        )
        present_counts: list[int] = [
            get_present_count(ds, serial) for serial in serials
        ]
        assistant_name: str = (
            group_data.loc[group_data[SERIAL] == assistant, NAME].astype(str).iloc[0]
        )

        leader_serials.append(leader)
        leader_names.append(leader_name)
        leader_groups.append(group)

        assistant_serials.append(assistant)
        assistant_names.append(assistant_name)

        group_data["Count"] = present_counts
        group_data[GENDER] = genders
        group_data["Potential Leader"] = [
            "True" if serial in leaders else "False" for serial in serials
        ]
        group_data["Potential Assistant Leader"] = [
            "True" if serial in assistants else "False" for serial in serials
        ]
        group_data["Leader"] = [
            "Leader" if serial == leader else "" for serial in serials
        ]
        group_data["Assistant"] = [
            "Assistant Leader" if serial == assistant else "" for serial in serials
        ]
        criterion_path = get_criterion_path()
        criterion_path.mkdir(exist_ok=True)
        DataStream(group_data).to_excel(get_group_criterion_path(group))

    leaders = pd.DataFrame(
        data={SERIAL: leader_serials, "Leader Name": leader_names, GROUP: leader_groups}
    )

    assistants = pd.DataFrame(
        data={
            SERIAL: assistant_serials,
            "Assistant Leader Name": assistant_names,
            GROUP: leader_groups,
        }
    )

    leaders = DataStream(leaders)
    leaders.to_excel(get_leader_path("Leader"))
    leaders.to_excel(get_grading_leader("Leader"))
    assistants = DataStream(assistants)
    assistants.to_excel(get_leader_path("Assistant"))
    assistants.to_excel(get_grading_leader("Assistant"))

    return Result[Unit].unit()
