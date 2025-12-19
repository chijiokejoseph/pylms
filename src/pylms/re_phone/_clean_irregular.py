from ..constants import SEMI_DELIM, SPACE_DELIM


def clean_irregular_space(entry: str) -> str:
    entry = entry.replace(SPACE_DELIM, "")
    return f"{entry}{SEMI_DELIM}".strip()


def clean_composite_irregular(entry: str, delim: str) -> str:
    if delim != SPACE_DELIM:
        entries: list[str] = entry.split(delim)
        output: str = ""
        for each_entry in entries:
            output += clean_irregular_space(each_entry) + SPACE_DELIM
        return output.strip()
    else:
        entry = entry.replace(SPACE_DELIM, "")
        output = ""
        for i in range(0, len(entry), 11):
            num_slice: slice = slice(i, i + 10)
            each_entry = entry[num_slice]
            output += f"{each_entry}{SEMI_DELIM}"
        return output.strip()
