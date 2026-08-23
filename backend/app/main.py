from fastapi import FastAPI
from .database import engine, Base
from .routes import auth

# Auto-generate tables in SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Siddique AI", version="1.0.0")

app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Siddque AI Backend"}