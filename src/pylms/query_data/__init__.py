"""Selectors package for querying and selecting students."""

from .interactive import combined_search, search_data
from .pipeline import apply_selector_pipeline
from .print_selection import print_selection
from .query import run_query_data
from .query_parse import query_parse
from .search_completion import search_completion
from .search_gender import search_gender
from .search_internship import search_internship
from .search_name import search_name
from .search_path import search_path
from .search_serials import search_serials
from .select_completion import select_completion
from .select_gender import select_gender
from .select_internship import select_internship
from .select_name import select_name
from .select_serials import select_serials
from .selector_type import Selector

__all__ = [
    "Selector",
    "select_name",
    "select_serials",
    "select_internship",
    "select_completion",
    "select_gender",
    "search_name",
    "search_serials",
    "search_internship",
    "search_completion",
    "search_gender",
    "search_path",
    "search_data",
    "combined_search",
    "print_selection",
    "apply_selector_pipeline",
    "query_parse",
    "run_query_data",
]
