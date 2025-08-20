from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TruckBase(BaseModel):
    registration_number: str
    capacity_mt: Optional[float] = None
    km_driven: Optional[float] = 0
    permit_expiry: Optional[date] = None
    tax_info: Optional[str] = None

class TruckCreate(TruckBase): pass

class Truck(TruckBase):
    id: int
    class Config: from_attributes = True

class TripBase(BaseModel):
    truck_id: int
    date: date
    origin: Optional[str] = None
    destination: Optional[str] = None
    distance_km: float = 0
    load_mt: float = 0
    rate_per_mt: float = 0
    income: Optional[float] = 0
    expenditure: Optional[float] = 0
    notes: Optional[str] = None

class TripCreate(TripBase): pass

class Trip(TripBase):
    id: int
    class Config: from_attributes = True

class ExpenseBase(BaseModel):
    trip_id: int
    category: str
    amount: float
    notes: Optional[str] = None

class ExpenseCreate(ExpenseBase): pass

class Expense(ExpenseBase):
    id: int
    class Config: from_attributes = True

class DocumentBase(BaseModel):
    truck_id: int
    doc_type: str
    number: Optional[str] = None
    issued_date: Optional[date] = None
    expiry_date: Optional[date] = None
    file_url: Optional[str] = None

class DocumentCreate(DocumentBase): pass

class Document(DocumentBase):
    id: int
    class Config: from_attributes = True

class TruckStats(BaseModel):
    truck_id: int
    registration_number: str
    total_trips: int
    total_km: float
    total_load_mt: float
    total_income: float
    total_expense: float
    profit: float
