import pandas as pd
from pylms.constants import DATA_COLUMNS, NAME, GROUP, SCORE


def validate_attendance(test_data: pd.DataFrame) -> bool:
    for column in DATA_COLUMNS:
        if column not in test_data.columns.tolist():
            return False
    return True


def validate_groups(test_data: pd.DataFrame) -> bool:
    for column in [NAME, GROUP]:
        if column not in test_data.columns.tolist():
            return False
    return True


def validate_scores(test_data: pd.DataFrame) -> bool:
    for column in [GROUP, SCORE]:
        if column not in test_data.columns.tolist():
            return False
    return True
