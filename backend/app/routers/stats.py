from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas
from ..deps import get_current_user

router = APIRouter(prefix='/api/stats', tags=['Stats'])

@router.get('/per_truck', response_model=list[schemas.TruckStats])
def stats_per_truck(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    trucks = db.query(models.Truck).filter(models.Truck.owner_id == user.id).all()
    results = []
    for t in trucks:
        total_trips = db.query(models.Trip).filter(models.Trip.truck_id == t.id).count()
        total_km = db.query(func.coalesce(func.sum(models.Trip.distance_km), 0.0)).filter(models.Trip.truck_id == t.id).scalar() or 0.0
        total_load = db.query(func.coalesce(func.sum(models.Trip.load_mt), 0.0)).filter(models.Trip.truck_id == t.id).scalar() or 0.0
        total_income = db.query(func.coalesce(func.sum(models.Trip.income), 0.0)).filter(models.Trip.truck_id == t.id).scalar() or 0.0
        total_expense = db.query(func.coalesce(func.sum(models.Expense.amount), 0.0)).join(models.Trip, models.Expense.trip_id == models.Trip.id).filter(models.Trip.truck_id == t.id).scalar() or 0.0
        results.append(schemas.TruckStats(
            truck_id=t.id,
            registration_number=t.registration_number,
            total_trips=total_trips,
            total_km=float(total_km),
            total_load_mt=float(total_load),
            total_income=float(total_income),
            total_expense=float(total_expense),
            profit=float(total_income - total_expense),
        ))
    return results
