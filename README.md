# Energy Billing System

A full-stack web application for managing electricity consumption data, generating invoices, and creating PDF bills. Built with FastAPI backend and Vue.js frontend.

## Quick Docker Setup (Recommended)

````bash
# Build and run the entire application
docker-compose up --build

# Stop the application
docker-compose down

# Rebuild if you updated .env or dependencies
docker-compose build --no-cache


## Technologies Used

### Backend

- **FastAPI** == 0.104.1
- **Uvicorn** == 0.24.0
- **SQLAlchemy** == 2.0.23
- **Pandas** == 2.1.3
- **Python-multipart** == 0.0.6
- **Jinja2** == 3.1.2
- **XHTML2PDF** == 0.2.11
- **SQLite** database

### Frontend

- **Vue 3** + Composition API
- **Vite** for build tooling
- **Vue Router** for navigation
- **Vue3-toastify** for notifications
- **Fetch API** for HTTP requests

##  Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Run entire application with Docker
docker-compose up
````

### MANUAL START

### BACKEND - Terminal 1

# Create virtual environment

python -m venv venv

# Activate venv (Windows)

venv\Scripts\activate

# Activate venv (Mac/Linux)

source venv/bin/activate

# Install dependencies

pip install -r requirements.txt

# Run backend server

uvicorn main:app --reload --host 0.0.0.0 --port 8000

### FRONTEND - Terminal 2

# Navigate to frontend

cd frontend

# Install dependencies

npm install

# Run frontend development server

npm run dev

# Delete database and restart

rm energy.db
docker-compose down
docker-compose up

# Access points

Frontend Application: http://localhost:5173

Backend API: http://localhost:8000

# Notes

Backend accepts csv files with sturcture as provided in the examples
