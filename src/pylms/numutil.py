from collections.abc import Iterable, Sized

from typing_extensions import Any


def det_num_width(num: Any) -> int:
    return len(str(num))


def max_index_width(values: Sized) -> int:
    return det_num_width(len(values))


def max_content_width(values_in: Iterable[Any]) -> int:
    values = [str(value) for value in values_in]
    counts = [len(value) for value in values]
    count_max = max(counts)
    return count_max
