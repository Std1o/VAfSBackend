from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from src.vafs import tables
from src.vafs.database import get_session
from src.vafs.models.auth import User
from src.vafs.models.event import Event, BaseEvent


class EventService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, user_id: int, event_data: BaseEvent) -> Event:
        event_dict = event_data.dict()
        event_dict['user_id'] = user_id
        event = tables.Event(**event_dict)
        self.session.add(event)
        self.session.commit()
        return event

    def get_event(self, event_id: int) -> Event:
        event = self.session.query(tables.Event).filter(tables.Event.id == event_id).first()
        return event

    def get_last_event(self, user_id: int) -> Event:
        event = self.session.query(tables.Event).filter(tables.Event.user_id == user_id).order_by(tables.Event.id.desc()).first()
        return event

    def get_events(self, user_id: int) -> List[Event]:
        event = self.session.query(tables.Event).filter(tables.Event.user_id == user_id).all()
        return event

