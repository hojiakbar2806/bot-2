from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteDead(StatesGroup):
    file = State()


class SearchUser(StatesGroup):
    user = State()


class AdminsActions(StatesGroup):
    add = State()
    delete = State()


class RequestsAdd(StatesGroup):
    channel_id = State()
    post = State()
    accept = State()


class RequestsDelete(StatesGroup):
    channel_id = State()


class RequestsChangePost(StatesGroup):
    post = State()


class CreateMailing(StatesGroup):
    post = State()
    date = State()
    pin = State()


class RefUrl(StatesGroup):
    create = State()
    delete = State()


class RequiredSubAdd(StatesGroup):
    channel_id = State()
    channel_url = State()
    verify = State()


class RequiredSubURL(StatesGroup):
    new_url = State()


class ButtonsURL(StatesGroup):
    new_url = State()


class UserMessage(StatesGroup):
    msg = State()


class ChangePaymentAmount(StatesGroup):
    new_amount = State()


class ChangeToken(StatesGroup):
    token = State()


class ChangeNumber(StatesGroup):
    number = State()


class ChangeNickname(StatesGroup):
    nickname = State()


class ChangeCPName(StatesGroup):
    new_name = State()
