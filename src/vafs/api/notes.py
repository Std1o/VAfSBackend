from typing import List

from fastapi import APIRouter, Depends
from src.vafs.models.auth import UserCreate, User, PrivateUser
from fastapi.security import OAuth2PasswordRequestForm

from src.vafs.models.event import Event, BaseEvent
from src.vafs.models.note import Note, BaseNote
from src.vafs.services.auth import AuthService, get_current_user
from src.vafs.services.events import EventService
from src.vafs.services.notes import NotesService
from src.vafs.services.user import UserService

router = APIRouter(prefix='/notes')

@router.get('/get_notes', response_model=List[Note])
def get_notes(user: User = Depends(get_current_user), service: NotesService = Depends()):
    return service.get_notes(user.id)

@router.post('/create_note', response_model=Note)
def create_note(note: BaseNote, user: User = Depends(get_current_user), service: NotesService = Depends()):
    return service.create(user.id, note)

@router.post('/update', response_model=Note)
def update_note(note: Note, user: User = Depends(get_current_user), service: NotesService = Depends()):
    return service.update(note)