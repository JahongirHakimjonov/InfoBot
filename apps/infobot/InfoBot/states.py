from aiogram.dispatcher.filters.state import StatesGroup, State


class PartnershipForm(StatesGroup):
    full_name = State()
    phone = State()
    address = State()
    user_message = State()


class InvestmentForm(StatesGroup):
    full_name = State()
    phone = State()
    address = State()
    user_message = State()
