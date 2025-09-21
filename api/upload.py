from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from database import get_db
from sqlalchemy.orm import Session
from datetime import datetime

import models
import pandas as pd
import uuid

router = APIRouter(prefix='/upload', tags=['upload'])
# upload CSV


@router.post("/{customer_id}")
async def upload_consumption_data(
    customer_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:
        db_customer = db.query(models.Customer).filter(
            models.Customer.id == customer_id).first()
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        try:
            df = pd.read_csv(
                file.file,
                delimiter=';',
                decimal=',',
                encoding='utf-8'
            )
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error reading CSV: {str(e)}")

        expected_columns = [
            'Časovna Značka (CEST/CET)', 'Poraba [kWh]', 'Dinamične Cene [EUR/kWh]']
        if not all(col in df.columns for col in expected_columns):
            raise HTTPException(
                status_code=400, detail=f"CSV must contain columns: {expected_columns}")

        new_records = []
        period_from = None
        period_to = None

        for index, row in df.iterrows():
            try:
                timestamp_str = row['Časovna Značka (CEST/CET)'].split('+')[0]
                timestamp = datetime.strptime(
                    timestamp_str, "%Y-%m-%dT%H:%M:%S")

                if period_from is None or timestamp < period_from:
                    period_from = timestamp
                if period_to is None or timestamp > period_to:
                    period_to = timestamp

                consumption = models.Consumption(
                    id=str(uuid.uuid4()),
                    timestamp=timestamp,
                    usage_kwh=row['Poraba [kWh]'],
                    price_eur=row['Dinamične Cene [EUR/kWh]'],
                    customer_id=customer_id
                )
                new_records.append(consumption)
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                continue

        if new_records:
            db.add_all(new_records)
            db.commit()

            return {
                "message": "CSV successfully uploaded!",
                "customer_id": customer_id,
                "records_processed": len(new_records),
                "period_from": period_from.isoformat() if period_from else None,
                "period_to": period_to.isoformat() if period_to else None,
                "customer_name": db_customer.name,
                "customer_email": db_customer.email
            }
        else:
            raise HTTPException(
                status_code=400, detail="No valid records found to upload.")

    finally:
        await file.close()
