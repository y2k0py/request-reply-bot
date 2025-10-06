from aiogram.fsm.state import StatesGroup, State

class CrateMessageWithButtonState(StatesGroup):
    set_message = State()
    set_button_text = State()
    set_button_url = State()
