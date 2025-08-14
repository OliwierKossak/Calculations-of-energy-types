from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import auth, data

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(data.router)
