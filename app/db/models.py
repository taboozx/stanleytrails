from sqlalchemy import Column, Integer, String, Date, Enum
from app.db.base import Base
import enum
import datetime

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
