from pydantic import BaseModel

class BaseEvent(BaseModel):
    title: str
    date: str

class Event(BaseEvent):
    id: int
    user_id: int