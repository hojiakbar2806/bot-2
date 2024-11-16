from sqlalchemy import Boolean, Column, BigInteger, JSON

from tg_bot.db_api.session import Base


class Requests(Base):
    __tablename__ = "requests"

    channel_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    message_id = Column(BigInteger, default=-1, nullable=False)
    message_chat_id = Column(BigInteger, default=-1, nullable=False)
    reply_markup = Column(JSON, default=None, nullable=True)
    accept_request = Column(Boolean, default=True, nullable=False)
