from typing import List

from fastapi import APIRouter, Depends
from src.vafs.models.auth import UserCreate, User, PrivateUser
from fastapi.security import OAuth2PasswordRequestForm

from src.vafs.models.event import Event, BaseEvent
from src.vafs.services.auth import AuthService, get_current_user
from src.vafs.services.events import EventService
from src.vafs.services.user import UserService

router = APIRouter(prefix='/events')


@router.post('/create_event', response_model=Event)
def create_event(event: BaseEvent, user: User = Depends(get_current_user), service: EventService = Depends()):
    return service.create(user.id, event)

@router.get('/get_event', response_model=Event)
def get_event(event_id: int, user: User = Depends(get_current_user), service: EventService = Depends()):
    return service.get_event(event_id)

@router.get('/get_events', response_model=List[Event])
def get_events(user: User = Depends(get_current_user), service: EventService = Depends()):
    return service.get_events(user.id)