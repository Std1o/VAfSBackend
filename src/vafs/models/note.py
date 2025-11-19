from pydantic import BaseModel

class BaseNote(BaseModel):
    title: str
    description: str

class Note(BaseNote):
    id: int
    user_id: int