from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..deps import get_current_user

router = APIRouter(prefix='/api/trips', tags=['Trips'])

@router.post('/', response_model=schemas.Trip)
def create_trip(trip: schemas.TripCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    t = db.query(models.Truck).filter(models.Truck.id == trip.truck_id, models.Truck.owner_id == user.id).first()
    if not t:
        raise HTTPException(status_code=404, detail='Truck not found')
    db_obj = models.Trip(**trip.model_dump())
    db.add(db_obj); db.commit(); db.refresh(db_obj); return db_obj

@router.get('/', response_model=list[schemas.Trip])
def list_trips(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return (db.query(models.Trip)
            .join(models.Truck, models.Trip.truck_id == models.Truck.id)
            .filter(models.Truck.owner_id == user.id)
            .order_by(models.Trip.date.desc())
            .all())
