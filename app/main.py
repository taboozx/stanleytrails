from fastapi import FastAPI
from app.db.base import Base
from app.db.db import engine
from app.db.db import SessionLocal
from app.api.contest import router as contest_router

from app.db.db import SessionLocal
from app.db.models import Hashtag, ApprovedUser
import json


app = FastAPI()

# создаём таблицы
Base.metadata.create_all(bind=engine)

# роуты
app.include_router(contest_router)
