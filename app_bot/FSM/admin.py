from aiogram.fsm.state import State, StatesGroup


class AdminScreamReview(StatesGroup):
    reviewing = State()
