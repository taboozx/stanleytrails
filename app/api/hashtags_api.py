from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.db import SessionLocal
from app.db.models import Hashtag

router = APIRouter()

@router.get("/hashtags")
def get_popular_hashtags():
    db: Session = SessionLocal()
    try:
        tags = db.query(Hashtag).order_by(Hashtag.count.desc()).limit(20).all()
        return [{"tag": h.tag.lstrip("#"), "count": h.count} for h in tags]
    finally:
        db.close()
