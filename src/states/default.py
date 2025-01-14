from aiogram.fsm.state import State, StatesGroup


class PaymentsStates(StatesGroup):
    get_amount = State()
    wait_payment = State()