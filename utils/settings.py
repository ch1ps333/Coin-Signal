from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    change_lang = State()
    change_threshold_ancreas = State()
    change_threshold_degreas = State()
    change_signal_step = State()
    change_rollback_threshold = State()
    change_rollback_step = State()
    change_signal_interval = State()
    change_rollback_interval = State()
    change_mail = State()
    