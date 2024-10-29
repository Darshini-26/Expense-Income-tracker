from fastapi import FastAPI
from fastapi import Depends
from src.database import SessionLocal, engine
import src.models as models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/income/", response_model=Income)
def create_income(income: IncomeCreate, db: Session = Depends(get_db)):
    db_income = Income(**income.dict())
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income