from pydantic import BaseModel
from datetime import datetime


# ------------------- Customer Schemas -------------------
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str

    address: str
    city: str
    postal_number: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: str

    class Config:
        from_attributes = True


# ------------------- Consumption Schemas -------------------
class ConsumptionBase(BaseModel):
    timestamp: datetime
    usage_kwh: float
    price_eur: float


class ConsumptionCreate(ConsumptionBase):
    customer_id: str


class Consumption(ConsumptionBase):
    id: str
    customer_id: str

    class Config:
        from_attributes = True


# ------------------- Invoice Schemas -------------------
class InvoiceBase(BaseModel):
    period_from: datetime
    period_to: datetime
    total_cost: float
    total_consumption_kwh: float


class InvoiceCreate(BaseModel):
    customer_id: str
    period_from: datetime
    period_to: datetime


class Invoice(InvoiceBase):
    id: str
    customer: Customer

    class Config:
        from_attributes = True
