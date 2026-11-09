from fastapi import FastAPI

app = FastAPI(title="FastAPI Calculator Database API")

@app.get("/")
def root():
    return {"status": "running", "message": "FastAPI Calculator connected with PostgreSQL"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
