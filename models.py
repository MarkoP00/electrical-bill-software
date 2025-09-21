from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

import uuid


class Customer(Base):
    __tablename__ = "customers"
    id = Column(String(36), primary_key=True,
                default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)

    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    postal_number = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    consumptions = relationship("Consumption", back_populates="customer")
    invoices = relationship("Invoice", back_populates="customer")


class Consumption(Base):
    __tablename__ = "consumptions"
    id = Column(String(36), primary_key=True,
                index=True)
    timestamp = Column(DateTime, nullable=False)
    usage_kwh = Column(Float, nullable=False)
    price_eur = Column(Float, nullable=False)

    customer_id = Column(String(36), ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="consumptions")


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(String(36), primary_key=True,
                default=lambda: str(uuid.uuid4()), index=True)
    total_cost = Column(Float, nullable=False)
    total_consumption_kwh = Column(Float, nullable=False)
    period_from = Column(DateTime, nullable=False)
    period_to = Column(DateTime, nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="invoices")
