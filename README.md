# FastAPI Calculator Project (Module 11)

This repository contains my FastAPI project with User and Calculation models, Pydantic schemas, a simple Factory pattern, and automated tests using GitHub Actions.

## Docker Hub Link

- https://hub.docker.com/r/opspiano/fastapi_calculator

## How to Run Tests Locally

1. Start the PostgreSQL database:

    docker-compose up -d db

2. Install required packages:

    pip install -r requirements.txt

3. Run pytest:

    DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db pytest -v
