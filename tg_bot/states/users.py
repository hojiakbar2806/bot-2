from aiogram.dispatcher.filters.state import State, StatesGroup


class DepositQiwiApi(StatesGroup):
    amount = State()


class DepositQiwiP2P(StatesGroup):
    amount = State()


class DepositCrystalPay(StatesGroup):
    amount = State()


class DepositLolz(StatesGroup):
    amount = State()


class Registration(StatesGroup):
    sex = State()
    age = State()


class Chat(StatesGroup):
    msg = State()


class ChooseSex(StatesGroup):
    sex = State()
