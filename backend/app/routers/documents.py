import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..deps import get_current_user
from typing import Optional
from datetime import date
from dotenv import load_dotenv

load_dotenv()
FILE_STORAGE_DIR = os.getenv('FILE_STORAGE_DIR', './uploaded_docs')
os.makedirs(FILE_STORAGE_DIR, exist_ok=True)

router = APIRouter(prefix='/api/documents', tags=['Documents'])

@router.post('/', response_model=schemas.Document)
async def create_document(
    truck_id: int = Form(...),
    doc_type: str = Form(...),
    number: Optional[str] = Form(None),
    issued_date: Optional[date] = Form(None),
    expiry_date: Optional[date] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    truck = db.query(models.Truck).filter(models.Truck.id == truck_id, models.Truck.owner_id == user.id).first()
    if not truck: raise HTTPException(status_code=404, detail='Truck not found')
    file_url = None
    if file:
        save_path = os.path.join(FILE_STORAGE_DIR, file.filename)
        with open(save_path, 'wb') as f:
            f.write(await file.read())
        file_url = save_path
    obj = models.Document(truck_id=truck_id, doc_type=doc_type, number=number, issued_date=issued_date, expiry_date=expiry_date, file_url=file_url)
    db.add(obj); db.commit(); db.refresh(obj); return obj

@router.get('/', response_model=list[schemas.Document])
def list_documents(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return (db.query(models.Document)
            .join(models.Truck, models.Document.truck_id == models.Truck.id)
            .filter(models.Truck.owner_id == user.id)
            .order_by(models.Document.id.desc())
            .all())
