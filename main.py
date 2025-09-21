from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, Base
from api import customers, invoices, upload

# uvicorn main:app --reload
app = FastAPI(
    title="Energy Management API",
    description="API for managing customers, consumptions, and invoices. Built with FastAPI, fully documented with OpenAPI.",
    version="1.0.0"
)


# only for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(customers.router)
app.include_router(invoices.router)
app.include_router(upload.router)

# test route


# @app.get("/ping")
# def ping():
#     return {"message": "pong"}
