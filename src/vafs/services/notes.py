from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from src.vafs import tables
from src.vafs.database import get_session
from src.vafs.models.auth import User
from src.vafs.models.event import Event, BaseEvent
from src.vafs.models.note import BaseNote


class NotesService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, user_id: int, note_data: BaseNote) -> Event:
        note_dict = note_data.dict()
        note_dict['user_id'] = user_id
        note = tables.Note(**note_dict)
        self.session.add(note)
        self.session.commit()
        return note

    def get_note(self, note_id: int) -> Event:
        note = self.session.query(tables.Event).filter(tables.Note.id == note_id).first()
        return note

    def get_last_note(self, user_id: int) -> Event:
        note = self.session.query(tables.Event).filter(tables.Note.user_id == user_id).order_by(tables.Note.id.desc()).first()
        return note

    def get_notes(self, user_id: int) -> List[Event]:
        event = self.session.query(tables.Note).filter(tables.Note.user_id == user_id).all()
        return event

