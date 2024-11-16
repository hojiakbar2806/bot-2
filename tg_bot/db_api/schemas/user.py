from datetime import datetime

from sqlalchemy import Boolean, Column, BigInteger, String, DateTime, Integer
from tg_bot.db_api.session import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    username = Column(String, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    registration_date = Column(DateTime, default=datetime.now)
    ban = Column(Boolean, default=False, nullable=False)
    referral_id = Column(BigInteger, default=0)
    registered = Column(Boolean, default=False)
    place = Column(String)
    sex = Column(String)
    age = Column(Integer, default=18)
    opposite_sex = Column(String, default="any")
    premium = Column(DateTime, default=None, nullable=True)
    rating = Column(Integer, default=0)
    total_dialogs = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
