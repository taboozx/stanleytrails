from sqlalchemy.orm import Session
from app.db.models import ContestWinner
from app.schemas.contest import ContestWinnerCreate

def create_winner(db: Session, data: ContestWinnerCreate):
    winner = ContestWinner(**data.dict())
    db.add(winner)
    db.commit()
    db.refresh(winner)
    return winner

def get_latest_winner(db: Session):
    return db.query(ContestWinner).order_by(ContestWinner.contest_date.desc()).first()
