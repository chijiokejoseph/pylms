from typing import Literal, NamedTuple, TypedDict

COLOR = "\x1b["
COLOR_BRIGHT = "\x1b[1;"


class Color(NamedTuple):
    bg: int
    text: int


class Palette(TypedDict):
    red: Color
    yellow: Color
    magenta: Color
    cyan: Color
    blue: Color
    green: Color
    white: Color
    default: Color


PALETTE: Palette = {
    "red": Color(bg=41, text=31),
    "green": Color(bg=42, text=32),
    "yellow": Color(bg=43, text=33),
    "blue": Color(bg=44, text=34),
    "magenta": Color(bg=45, text=35),
    "cyan": Color(bg=46, text=36),
    "white": Color(bg=47, text=37),
    "default": Color(bg=49, text=39),
}


def build(color: str, kind: Literal["bg", "text"], bold: bool) -> str | None:
    value: Color | None = PALETTE.get(color)
    if value is None:
        return value

    if kind == "bg":
        color = str(value.bg) + "m"
    else:
        color = str(value.text) + "m"

    if bold:
        return COLOR_BRIGHT + color
    else:
        return COLOR + color


def emphasis(sample: str, part: str | None = None) -> str:
    code = build("magenta", "text", True)
    reset = build("default", "text", False)
    assert code is not None, f"code: '{code} is None"
    assert reset is not None, f"reset: '{reset} is None"

    if part is not None:
        sample = sample.replace(part, f"{code}{part}{reset}")
    else:
        sample = f"{code}{sample}{reset}"

    return sample


if __name__ == "__main__":
    result = emphasis("I am hungry")
    print(f"{result = }")
    print(result)
