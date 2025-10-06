from aiogram.fsm.state import StatesGroup, State

class CreateMessageWithButtonState(StatesGroup):
    message = State()
    button = State()
