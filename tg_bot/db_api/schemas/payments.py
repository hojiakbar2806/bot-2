from datetime import datetime

from sqlalchemy import Boolean, Column, BigInteger, String, DateTime, Integer, ForeignKey
from tg_bot.db_api.session import Base


class Bill(Base):
    __tablename__ = "bills"

    bill_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    date = Column(DateTime, default=datetime.now)
    paid = Column(Boolean, default=True)
    amount = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)


class Deposits(Base):
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    date = Column(DateTime, default=datetime.now)
    paid = Column(Boolean, default=False)
    payment_system = Column(String)
    amount = Column(Integer, nullable=False)
    