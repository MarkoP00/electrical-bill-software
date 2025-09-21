from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import and_
from fastapi.responses import FileResponse
from jinja2 import Template
from datetime import datetime, timedelta
from xhtml2pdf import pisa
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv

import smtplib
import os
import models
import schemas

router = APIRouter(prefix='/invoices', tags=['invoices'])

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# create invoice - POST /invoices


@router.post("/", response_model=schemas.Invoice)
def create_invoice(invoice_data: schemas.InvoiceCreate, db: Session = Depends(get_db)):

    db_customer = db.query(models.Customer).filter(
        models.Customer.id == invoice_data.customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    consumptions = db.query(models.Consumption).filter(
        and_(
            models.Consumption.customer_id == invoice_data.customer_id,
            models.Consumption.timestamp >= invoice_data.period_from,
            models.Consumption.timestamp <= invoice_data.period_to
        )
    ).all()

    if not consumptions:
        raise HTTPException(
            status_code=404, detail="No consumption data found for this period")

    total_cost = 0.0
    total_consumption_kwh = 0.0

    for cons in consumptions:
        total_cost += cons.usage_kwh * cons.price_eur
        total_consumption_kwh += cons.usage_kwh

    db_invoice = models.Invoice(
        total_cost=round(total_cost, 2),
        total_consumption_kwh=round(
            total_consumption_kwh, 2),
        period_from=invoice_data.period_from,
        period_to=invoice_data.period_to,
        customer_id=invoice_data.customer_id
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    print(f" Račun uspešno generisan! ID: {db_invoice.id}")

    return db_invoice

# send invoice via email - POST /invoices/invoice_id/send


@router.post("/{invoice_id}/send")
async def send_invoice_email(
    invoice_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_invoice = db.query(models.Invoice).filter(
        models.Invoice.id == invoice_id).first()
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    pdf_filename = f"invoice_{invoice_id}.pdf"
    if not os.path.exists(pdf_filename):
        raise HTTPException(status_code=404, detail="PDF not generated yet")

    background_tasks.add_task(
        _send_email_with_attachment,
        db_invoice.customer.email,
        pdf_filename
    )

    return {"message": f"Invoice will be sent to {db_invoice.customer.email}"}



def _send_email_with_attachment(to_email: str, pdf_path: str):
    from_email = EMAIL_USER
    password = EMAIL_PASS

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "Your Invoice"

    msg.attach(MIMEText("Hello, please find your invoice attached.", "plain"))

    with open(pdf_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(pdf_path)}"
        )
        msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

# delete invoice - DELETE /invoices/invoice_id


@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: str, db: Session = Depends(get_db)):
    db_invoice = db.query(models.Invoice).filter(
        models.Invoice.id == invoice_id).first()

    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(db_invoice)
    db.commit()

    return {"message": f"Invoice {invoice_id} deleted successfully"}

# generate invoice - jinja2 - get /invoices/invoice_id/pdf


@router.get("/{invoice_id}/pdf")
async def generate_invoice_pdf(invoice_id: str, db: Session = Depends(get_db)):
    db_invoice = db.query(models.Invoice).filter(
        models.Invoice.id == invoice_id).first()
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    try:
        with open("templates/invoice.html", "r", encoding="utf-8") as f:
            template_str = f.read()
    except FileNotFoundError:
        raise HTTPException(
            status_code=500, detail="Invoice template not found")

    template = Template(template_str)
    html_content = template.render(
        invoice_number=db_invoice.id[:8].upper(),
        period_from=db_invoice.period_from.strftime("%d.%m.%Y"),
        period_to=db_invoice.period_to.strftime("%d.%m.%Y"),
        customer_id=db_invoice.customer.id[:8],
        customer_name=db_invoice.customer.name,
        customer_email=db_invoice.customer.email,
        customer_phone=db_invoice.customer.phone,
        customer_address=db_invoice.customer.address,
        customer_city=db_invoice.customer.city,
        customer_postal_number=db_invoice.customer.postal_number,
        total_cost=f"{db_invoice.total_cost:.2f}",
        total_consumption_kwh=f"{db_invoice.total_consumption_kwh:.2f}"
    )

    pdf_filename = f"invoice_{invoice_id}.pdf"

    try:
        with open(pdf_filename, "wb") as f:
            pisa.CreatePDF(html_content, dest=f)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"PDF generation failed: {str(e)}")

    return FileResponse(
        pdf_filename,
        media_type="application/pdf",
        filename=f"racun_{db_invoice.customer.name}_{db_invoice.period_from.strftime('%Y%m')}.pdf"
    )


# {
#   "customer_id": "d61dc8fe-c676-48ae-b9c1-3ba359e3afab",
#   "period_from": "2024-07-01T00:00:00",
#   "period_to": "2024-07-31T23:59:59"
# }
