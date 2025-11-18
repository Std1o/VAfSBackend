from fastapi import Depends
from sqlalchemy.orm import Session

from src.vafs import tables
from src.vafs.database import get_session
from src.vafs.models.auth import User


class UserService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def update_group(self, user_id: int, group: str) -> User:
        self.session.query(tables.User).filter(tables.User.id == user_id).update({"group": group})
        self.session.commit()
        user = self.session.query(tables.User).filter(tables.User.id == user_id).first()
        self.session.expire_all()
        return user

    def get_actual_user(self, user_id: int):
        user = self.session.query(tables.User).filter(tables.User.id == user_id).first()
        return user

