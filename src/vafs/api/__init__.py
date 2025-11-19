from fastapi import APIRouter
from .auth import router as auth_router
from .user import router as group_router
from .chat import router as chat_router
from .events import router as events_router
from .notes import router as notes_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(group_router)
router.include_router(chat_router)
router.include_router(events_router)
router.include_router(notes_router)