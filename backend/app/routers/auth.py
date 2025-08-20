from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db, Base, engine
from .. import models, schemas
from ..auth_utils import get_password_hash, verify_password, create_access_token

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix='/api/auth', tags=['Auth'])

@router.post('/register', response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.email == user.email).first()
    if exists:
        raise HTTPException(status_code=400, detail='Email already registered')
    hashed = get_password_hash(user.password)
    u = models.User(email=user.email, full_name=user.full_name, hashed_password=hashed)
    db.add(u); db.commit(); db.refresh(u)
    return u

@router.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token({'sub': user.email})
    return {'access_token': token, 'token_type': 'bearer'}
