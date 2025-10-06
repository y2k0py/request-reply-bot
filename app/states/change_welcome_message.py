from aiogram.fsm.state import StatesGroup, State

class ChangeWelcomeMessage(StatesGroup):
    change_message = State()
    change_button_text = State()
    change_button_url = State()
