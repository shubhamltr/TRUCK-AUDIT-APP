from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..deps import get_current_user

router = APIRouter(prefix='/api/trucks', tags=['Trucks'])

@router.post('/', response_model=schemas.Truck)
def create_truck(truck: schemas.TruckCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_obj = models.Truck(owner_id=user.id, **truck.model_dump())
    db.add(db_obj); db.commit(); db.refresh(db_obj); return db_obj

@router.get('/', response_model=list[schemas.Truck])
def list_trucks(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Truck).filter(models.Truck.owner_id == user.id).order_by(models.Truck.registration_number.asc()).all()
