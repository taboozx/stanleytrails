from pydantic import BaseModel
from datetime import date
from enum import Enum

class WinnerStatus(str, Enum):
    waiting = "waiting_contact"
    done = "done"

class ContestWinnerCreate(BaseModel):
    tg_id: str
    username: str
    score: int

class ContestWinnerOut(BaseModel):
    id: int
    tg_id: str
    username: str
    contest_date: date
    score: int
    status: WinnerStatus
    contact_info: str | None = None

    class Config:
        orm_mode = True
