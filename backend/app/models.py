from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    trucks = relationship("Truck", back_populates="owner", cascade="all, delete-orphan")

class Truck(Base):
    __tablename__ = "trucks"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    registration_number = Column(String(64), index=True, nullable=False)
    capacity_mt = Column(Float, nullable=True)
    km_driven = Column(Float, nullable=True, default=0.0)
    permit_expiry = Column(Date, nullable=True)
    tax_info = Column(String(255), nullable=True)

    owner = relationship("User", back_populates="trucks")
    trips = relationship("Trip", back_populates="truck", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="truck", cascade="all, delete-orphan")

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    truck_id = Column(Integer, ForeignKey("trucks.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    origin = Column(String(128), nullable=True)
    destination = Column(String(128), nullable=True)
    distance_km = Column(Float, nullable=False, default=0.0)
    load_mt = Column(Float, nullable=False, default=0.0)
    rate_per_mt = Column(Float, nullable=False, default=0.0)
    income = Column(Float, nullable=True, default=0.0)
    expenditure = Column(Float, nullable=True, default=0.0)
    notes = Column(Text, nullable=True)

    truck = relationship("Truck", back_populates="trips")
    expenses = relationship("Expense", back_populates="trip", cascade="all, delete-orphan")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False, index=True)
    category = Column(String(64), nullable=False)
    amount = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)

    trip = relationship("Trip", back_populates="expenses")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    truck_id = Column(Integer, ForeignKey("trucks.id"), nullable=False, index=True)
    doc_type = Column(String(64), nullable=False)
    number = Column(String(128), nullable=True)
    issued_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    file_url = Column(String(512), nullable=True)
    uploaded_at = Column(DateTime, server_default=func.now())

    truck = relationship("Truck", back_populates="documents")
