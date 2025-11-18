from pydantic import BaseModel


class Event(BaseModel):
    id: int
    user_id: int
    title: str
    date: str