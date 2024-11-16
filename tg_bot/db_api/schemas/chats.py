from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime

from tg_bot.db_api.session import Base


class Chats(Base):
    __tablename__ = "chats"

    chat_id = Column(BigInteger, primary_key=True, nullable=False)
    registration_date = Column(DateTime, default=datetime.now)
