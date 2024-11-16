from sqlalchemy import Column, String
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

from tg_bot.db_api.session import Base


class ReferralUrls(Base):
    __tablename__ = "refurls"

    name = Column(String, primary_key=True, index=True, nullable=False)
    users = Column(MutableList.as_mutable(PickleType),
                   default=[])
    chats = Column(MutableList.as_mutable(PickleType),
                   default=[])
