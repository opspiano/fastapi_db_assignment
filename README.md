# FastAPI Calculator Project (Module 12)

FastAPI app with user register/login routes and calculation BREAD endpoints.

## Docker Hub

- https://hub.docker.com/r/opspiano/fastapi_calculator

## Run Tests Locally

1. Start PostgreSQL:

    docker-compose up -d db

2. Run pytest:

    DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db pytest -v

## Manual Check via OpenAPI

1. Start server:

    DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db uvicorn app.main:app --reload

2. Open http://localhost:8000/docs in a browser and test the endpoints.
