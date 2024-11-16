from sqlalchemy import Boolean, Column, BigInteger, String, Integer
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

from tg_bot.db_api.session import Base


class RequiredSub(Base):
    __tablename__ = "required_subs"

    sid = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    channel_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    channel_url = Column(String)
    verify = Column(Boolean, nullable=False)
    users_subbed = Column(MutableList.as_mutable(PickleType),
                          default=[])
