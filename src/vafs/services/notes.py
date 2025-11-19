from typing import List

from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.vafs import tables
from src.vafs.database import get_session
from src.vafs.models.auth import User
from src.vafs.models.note import BaseNote, Note


class NotesService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, user_id: int, note_data: BaseNote) -> Note:
        note_dict = note_data.dict()
        note_dict['user_id'] = user_id
        note = tables.Note(**note_dict)
        self.session.add(note)
        self.session.commit()
        return note

    def get_note(self, note_id: int) -> Note:
        note = self.session.query(tables.Note).filter(tables.Note.id == note_id).first()
        return note

    def get_notes(self, user_id: int) -> List[Note]:
        note = self.session.query(tables.Note).filter(tables.Note.user_id == user_id).all()
        return note

    def update(self, note: Note) -> Note:
        stmt = update(tables.Note).where(tables.Note.id == note.id).values(
            title=note.title,
            description=note.description,
        )
        self.session.execute(stmt)
        self.session.commit()
        note = self.session.query(tables.Note).filter(tables.Note.id == note.id).first()
        self.session.expire_all()
        return note

