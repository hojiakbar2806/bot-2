from datetime import datetime

from sqlalchemy import Boolean, Column, BigInteger, String, DateTime, Integer
from tg_bot.db_api.session import Base


class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_user_id = Column(BigInteger, index=True)
    second_user_id = Column(BigInteger, index=True)
    started = Column(DateTime, default=datetime.now)
