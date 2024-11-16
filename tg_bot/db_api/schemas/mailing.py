from sqlalchemy import Boolean, Column, BigInteger, String, DateTime, JSON, Integer

from tg_bot.db_api.session import Base


class Mailing(Base):
    __tablename__ = "mailings"

    job_id = Column(String, primary_key=True, index=True, nullable=False)
    message_id = Column(BigInteger)
    message_chat_id = Column(BigInteger)
    markup = Column(JSON)
    run_date = Column(DateTime)
    active = Column(Boolean, default=True, nullable=False)
    total = Column(Integer, default=0, nullable=False)
    success = Column(Integer, default=0, nullable=False)
    failed = Column(Integer, default=0, nullable=False)
