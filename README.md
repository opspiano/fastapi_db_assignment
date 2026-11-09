# FastAPI Secure User Management & CI/CD Pipeline

This project implements a secure user authentication backend using FastAPI, SQLAlchemy ORM, and Pydantic validation. The deployment and testing lifecycle is automated through GitHub Actions and Docker Hub.

## Features
- SQLAlchemy User Model: Persistent database model storing hashed passwords with unique constraints on username and email.
- Pydantic Validation: Input data validation and serialization preventing invalid records from hitting the database.
- Password Hashing: Bcrypt-based salting and hashing mechanisms.
- Automated Testing: Pytest suite executing unit tests and database integration tests against a PostgreSQL container.
- CI/CD Automation: GitHub Actions workflow testing code on PR/push and publishing Docker images to Docker Hub.

## Docker Hub Repository
- Image Repository: https://hub.docker.com/r/opspiano/fastapi_calculator

## Running Tests Locally

### Prerequisites
- Python 3.10+
- Running PostgreSQL database instance

### Setup and Execution
1. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Configure DATABASE_URL and run tests:
   export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/fastapi_db"
   pytest -v