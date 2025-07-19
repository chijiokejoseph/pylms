from dataclasses import dataclass, field
from typing import TypedDict


@dataclass
class Form:
    title: str
    name: str
    url: str = field(default="")
    uuid: str = field(default="")


class FormInfo(TypedDict):
    title: str
    document_title: str


class FormData(TypedDict, total=False):
    info: FormInfo


class PermissionsData(TypedDict, total=False):
    type: str
    role: str
    emailAddress: str
