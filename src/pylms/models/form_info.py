from pydantic import BaseModel


class ClassFormInfo(BaseModel):
    date: str
    present_name: str
    present_title: str
    present_url: str
    present_id: str
    excused_name: str
    excused_title: str
    excused_url: str
    excused_id: str
    timestamp: str


class UpdateFormInfo(BaseModel):
    week_num: int
    year_num: int
    name: str
    title: str
    url: str
    uuid: str
    dates: list[str]
    timestamp: str


class CDSFormInfo(BaseModel):
    name: str
    title: str
    url: str
    uuid: str
    timestamp: str
