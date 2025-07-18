from pydantic import BaseModel


class UpdateFormRecord(BaseModel):
    name: str
    title: str
    marked: bool
