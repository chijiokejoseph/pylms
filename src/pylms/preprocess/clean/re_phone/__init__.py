from typing import Callable
from pylms.preprocess.clean.re_phone._re_match import _re_match


def match_and_clean(entry: str) -> str:
    entry = entry.strip()
    func: Callable[[str], str] = _re_match(entry)
    return func(entry)


__all__ = [
    "match_and_clean",
]
