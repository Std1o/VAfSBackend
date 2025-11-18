from fastapi import APIRouter, Depends
from src.vafs.models.auth import UserCreate, User, PrivateUser
from fastapi.security import OAuth2PasswordRequestForm

from src.vafs.services.auth import AuthService, get_current_user
from src.vafs.services.user import UserService

router = APIRouter(prefix='/user')


@router.post('/update_group', response_model=User)
def update_group(group: str, user: User = Depends(get_current_user), service: UserService = Depends()):
    return service.update_group(user.id, group)

@router.get('/user', response_model=User)
def get_user(user: User = Depends(get_current_user), service: UserService = Depends()):
    return service.get_actual_user(user.id)