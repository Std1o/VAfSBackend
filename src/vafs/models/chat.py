from pydantic import BaseModel


class ChatItem(BaseModel):
    message: str
    date: str