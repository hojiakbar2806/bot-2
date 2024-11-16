from datetime import datetime

from sqlalchemy import Boolean, Column, BigInteger, String, DateTime, Integer
from tg_bot.db_api.session import Base


class Queue(Base):
    __tablename__ = "search_queue"

    user_id = Column(BigInteger, primary_key=True)
    sex = Column(String)
    opposite_sex = Column(String)
    age = Column(Integer)
    added_time = Column(DateTime, default=datetime.now)
