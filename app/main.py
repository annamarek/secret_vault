from fastapi import FastAPI

from .database import Base, engine
from .routers import auth, secrets

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secret Vault API"
)

app.include_router(auth.router)
app.include_router(secrets.router)