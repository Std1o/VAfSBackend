from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Depends
from fastapi import WebSocket, WebSocketDisconnect
from starlette import status

from src.vafs.models.chat import ChatItem
from src.vafs.models.event import BaseEvent
from src.vafs.models.note import BaseNote
from src.vafs.services.auth import get_current_user
from src.vafs.services.events import EventService
from src.vafs.services.notes import NotesService

router = APIRouter()


class Storage:
    def __init__(self):
        self.notes: List[Dict] = []
        self.events: List[Dict] = []
        self.user_states: Dict[str, Dict] = {}

    def add_note(self, title: str, description: str):
        self.notes.append({
            "title": title,
            "description": description,
            "created_at": datetime.now().isoformat()
        })

    def add_event(self, date: str, event: str):
        self.events.append({
            "date": date,
            "event": event,
            "created_at": datetime.now().isoformat()
        })

    def get_events_by_date(self, date: str) -> List[Dict]:
        return [event for event in self.events if event["date"] == date]


storage = Storage()


class ChatBot:
    def __init__(self):
        self.states = {}

    async def send_response(self, websocket: WebSocket, mode: str, message: str):
        """Универсальный метод для отправки ответа"""
        response = {
            "mode": mode,
            "message": message
        }
        await websocket.send_json(response)

    async def handle_message(self, websocket: WebSocket, message: str, user_id: int, event_service: EventService,
                             note_service: NotesService):
        # Инициализация состояния пользователя
        if user_id not in self.states:
            self.states[user_id] = {"mode": None}

        state = self.states[user_id]

        # Обработка команды "назад"
        if message.lower() == "назад":
            state["mode"] = None
            # Очищаем все данные состояния
            keys_to_remove = [key for key in state.keys() if key not in ["mode"]]
            for key in keys_to_remove:
                del state[key]
            await self.send_response(websocket, "menu", "Опция отменена. Чем могу помочь?")
            return

        # Основное меню
        if state["mode"] is None:
            await self.handle_main_menu(websocket, message, state, user_id)
        # Режим расписания
        elif state["mode"] == "schedule":
            await self.handle_schedule(websocket, message, state, user_id)
        # Режим заметки
        elif state["mode"] == "note":
            await self.handle_note(websocket=websocket, message=message, state=state, user_id=user_id, note_service=note_service)
        # Режим календаря
        elif state["mode"] == "calendar":
            await self.handle_calendar(websocket, message, state, user_id, event_service)

    async def handle_main_menu(self, websocket: WebSocket, message: str, state: Dict, user_id: int):
        message_lower = message.lower()

        if any(word in message_lower for word in ["расписание", "расписания", "расписании"]):
            state["mode"] = "schedule"
            await self.send_response(
                websocket,
                "schedule",
                'Назовите дату в формате "01.01.2025"\nЕсли хотите отменить опцию, напишите "назад"'
            )

        elif any(word in message_lower for word in ["заметка", "заметку", "заметки"]):
            state["mode"] = "note"
            state["step"] = "title"
            await self.send_response(
                websocket,
                "note",
                'Назовите заголовок заметки:\nЕсли хотите отменить опцию, напишите "назад"'
            )

        elif any(word in message_lower for word in ["календарь", "календаре", "календарём"]):
            state["mode"] = "calendar"
            state["step"] = "ask_add_event"
            await self.send_response(
                websocket,
                "calendar_confirm",
                'Хотите добавить событие на определенную дату? Да/Нет\nЕсли хотите отменить опцию, напишите "назад"'
            )

        else:
            await self.send_response(
                websocket,
                "menu",
                "Добро пожаловать! Выберите опцию:\n"
                "1. Расписание - посмотреть события на дату\n"
                "2. Заметка - создать новую заметку\n"
                "3. Календарь - добавить событие в календарь"
            )

    async def handle_schedule(self, websocket: WebSocket, message: str, state: Dict, user_id: int):
        try:
            # Проверка формата даты
            datetime.strptime(message, "%d.%m.%Y")
            events = storage.get_events_by_date(message)

            await self.send_response(websocket, "schedule_result", message)
            state["mode"] = None

        except ValueError:
            await self.send_response(
                websocket,
                "schedule",
                'Неверный формат даты. Используйте формат "01.01.2025"\nЕсли хотите отменить опцию, напишите "назад"'
            )

    async def handle_note(self, websocket: WebSocket, message: str, state: Dict, user_id: int,
                          note_service: NotesService):
        step = state.get("step")

        if step == "title":
            state["title"] = message
            state["step"] = "description"
            await self.send_response(
                websocket,
                "note_description",
                'Опишите заметку:\nЕсли хотите отменить опцию, напишите "назад"'
            )

        elif step == "description":
            state["description"] = message
            note_service.create(user_id, BaseNote(title=state["title"], description=state["description"]))

            await self.send_response(
                websocket,
                "note_success",
                'Отлично! Заметка оформлена. Посмотреть ее можно во вкладке "Заметки".'
            )
            # Очищаем состояние
            state["mode"] = None
            if "title" in state: del state["title"]
            if "description" in state: del state["description"]
            if "step" in state: del state["step"]

    async def handle_calendar(self, websocket: WebSocket, message: str, state: Dict, user_id: int,
                              event_service: EventService):
        step = state.get("step")

        if step == "ask_add_event":
            if message.lower() == "да":
                state["step"] = "date"
                await self.send_response(
                    websocket,
                    "calendar_date",
                    'Назовите дату события в формате "01.01.2025"\nЕсли хотите отменить опцию, напишите "назад"'
                )
            elif message.lower() == "нет":
                state["mode"] = None
                if "step" in state: del state["step"]
                await self.send_response(websocket, "menu", "Возвращаюсь в главное меню")
            else:
                await self.send_response(
                    websocket,
                    "calendar_confirm",
                    'Пожалуйста, ответьте "Да" или "Нет"\nЕсли хотите отменить опцию, напишите "назад"'
                )

        elif step == "date":
            try:
                datetime.strptime(message, "%d.%m.%Y")
                state["date"] = message
                state["step"] = "event"
                await self.send_response(
                    websocket,
                    "calendar_event",
                    'Назовите событие:\nЕсли хотите отменить опцию, напишите "назад"'
                )
            except ValueError:
                await self.send_response(
                    websocket,
                    "calendar_date",
                    'Неверный формат даты. Используйте формат "01.01.2025"\nЕсли хотите отменить опцию, напишите "назад"'
                )

        elif step == "event":
            state["event"] = message
            event_service.create(user_id, BaseEvent(title=state["event"], date=state["date"]))
            state["step"] = "ask_open"
            await self.send_response(
                websocket,
                "calendar_open",
                'Отлично, событие записано в календарь, открыть его? Да/Нет\nЕсли хотите отменить опцию, напишите "назад"'
            )

        elif step == "ask_open":
            if message.lower() == "да":
                event = event_service.get_last_event(user_id)
                if event:
                    response_message = event.date
                else:
                    response_message = f"На {state['date']} событий нет."
                await self.send_response(websocket, "calendar_result", response_message)

            # Очищаем состояние
            state["mode"] = None
            keys_to_remove = [key for key in state.keys() if key not in ["mode"]]
            for key in keys_to_remove:
                del state[key]


chat_bot = ChatBot()


@router.websocket("/chat")
async def send_message(websocket: WebSocket, event_service: EventService = Depends(),
                       note_service: NotesService = Depends()):
    await websocket.accept()
    user = None
    try:
        token = websocket.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")

        token = token.split(" ")[1]  # Убираем "Bearer"
        user = get_current_user(token)

        while True:
            data = await websocket.receive_text()
            await chat_bot.handle_message(websocket, data, user.id, event_service, note_service)
    except WebSocketDisconnect:
        print(f"WebSocket connection closed")
    except Exception as e:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        print(f"Error in WebSocket connection: {e}")
