from fastapi import FastAPI
from app.database import engine
from app.routers import prediction, user
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(prediction.router)


