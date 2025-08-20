from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..deps import get_current_user

router = APIRouter(prefix='/api/expenses', tags=['Expenses'])

@router.post('/', response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    trip = (db.query(models.Trip)
            .join(models.Truck, models.Trip.truck_id == models.Truck.id)
            .filter(models.Trip.id == expense.trip_id, models.Truck.owner_id == user.id)
            .first())
    if not trip: raise HTTPException(status_code=404, detail='Trip not found')
    obj = models.Expense(**expense.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.get('/', response_model=list[schemas.Expense])
def list_expenses(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return (db.query(models.Expense)
            .join(models.Trip, models.Expense.trip_id == models.Trip.id)
            .join(models.Truck, models.Trip.truck_id == models.Truck.id)
            .filter(models.Truck.owner_id == user.id)
            .order_by(models.Expense.id.desc())
            .all())
