from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db import SessionLocal
from app.schemas.contest import ContestWinnerCreate, ContestWinnerOut
from app.crud.contest import create_winner, get_latest_winner

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/contest/run", response_model=ContestWinnerOut)
def run_contest(data: ContestWinnerCreate, db: Session = Depends(get_db)):
    return create_winner(db, data)

@router.get("/api/contest/latest", response_model=ContestWinnerOut)
def latest_winner(db: Session = Depends(get_db)):
    return get_latest_winner(db)
