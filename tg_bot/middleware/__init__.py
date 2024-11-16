from aiogram import Dispatcher

from .log import LogMiddleware
from .session import SessionMiddleware
from .throttling import ThrottlingMiddleware
from .required_sub import CheckSubMiddleware
from .ban import CheckBanMiddleware


def setup_middlewares(dp: Dispatcher):
    dp.setup_middleware(LogMiddleware())
    dp.setup_middleware(SessionMiddleware())
    dp.setup_middleware(ThrottlingMiddleware())
    dp.setup_middleware(CheckSubMiddleware())
    dp.setup_middleware(CheckBanMiddleware())
