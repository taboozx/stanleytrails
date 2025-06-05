from sqlalchemy import Column, Integer, String, Date, Enum
from app.db.base import Base

import enum
import datetime

print("🔍 models.py загружается!")

class WinnerStatus(str, enum.Enum):
    waiting = "waiting_contact"
    done = "done"

class ContestWinner(Base):
    __tablename__ = "contest_winners"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(String, unique=True)
    username = Column(String)
    contest_date = Column(Date, default=datetime.date.today)
    score = Column(Integer)
    contact_info = Column(String, nullable=True)
    status = Column(Enum(WinnerStatus), default=WinnerStatus.waiting)

class Hashtag(Base):
    __tablename__ = "hashtags"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, unique=True, index=True)
    count = Column(Integer, default=0)

# для учета последнего отсканированного поста, для разных нужд
class MetaKV(Base):
    __tablename__ = "meta_kv"
    key = Column(String, primary_key=True)
    value = Column(String)

class ApprovedUser(Base):
    __tablename__ = "approved_users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(String, unique=True)
    username = Column(String, nullable=True)



print("✅ модели успешно определены")