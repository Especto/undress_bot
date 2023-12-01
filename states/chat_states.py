from aiogram.fsm.state import StatesGroup, State


class ChatStates(StatesGroup):
     GetPhoto = State()
     AccountMenu = State()
     LangMenu = State()


