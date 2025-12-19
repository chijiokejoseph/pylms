from typing import Callable

from ._re_match import re_match


def match_and_clean(entry: str) -> str:
    entry = entry.strip()
    func: Callable[[str], str] = re_match(entry)
    return func(entry)


__all__ = [
    "match_and_clean",
]
