from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from typing import List

import models
import schemas

router = APIRouter(prefix="/customers", tags=['customers'])

# get all users - GET /customers


@router.get('/', response_model=list[schemas.Customer])
def get_all_customers(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return customers

# get single customer GET /customers/customer_id


@router.get("/{customer_id}", response_model=schemas.Customer)
def get_one_customer(customer_id: str, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id).first()

    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return db_customer

# create customer - POST /customers


@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    try:
        db_customer = models.Customer(
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
            address=customer.address,
            city=customer.city,
            postal_number=customer.postal_number
        )
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already in use"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating customer: {str(e)}"
        )

# get customers generated invoices - GET /customers/customer_id/invoices


@router.get('/{customer_id}/invoices', response_model=List[schemas.Invoice])
def get_customer_invoices(customer_id: str, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    invoices = db.query(models.Invoice).filter(
        models.Invoice.customer_id == customer_id
    ).all()

    return invoices
# update customer


@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: str,
    customer_update: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):

    db_customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id).first()

    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # email check
    if customer_update.email != db_customer.email:
        existing_customer = db.query(models.Customer).filter(
            models.Customer.email == customer_update.email).first()
        if existing_customer:
            raise HTTPException(status_code=400, detail="Email already in use")

    db_customer.name = customer_update.name
    db_customer.email = customer_update.email
    db_customer.phone = customer_update.phone
    db_customer.address = customer_update.address
    db_customer.city = customer_update.city
    db_customer.postal_number = customer_update.postal_number

    db.commit()
    db.refresh(db_customer)

    return db_customer


# DELETE customer
@router.delete("/{customer_id}")
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id).first()

    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(db_customer)
    db.commit()

    return {"message": "Customer deleted successfully"}
