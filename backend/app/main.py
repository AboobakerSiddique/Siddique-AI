from fastapi import FastAPI
from .database import engine, Base
from .routes import auth, chat

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Siddque AI", version="1.0.0")

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Siddque AI Backend"}
