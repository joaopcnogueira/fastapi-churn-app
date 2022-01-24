import joblib
import pandas as pd
from pathlib import Path

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from . import models, schemas, utils
from .database import engine, get_db
from fastapi.security import OAuth2PasswordBearer


BASE_DIR = Path('.')
models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


@app.post("/predict", response_model=schemas.CustomerResponse)
def predict(customer: schemas.Customer, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    customer_dict = customer.dict()
    customer_df = pd.DataFrame([customer_dict])
    model = joblib.load(BASE_DIR/'pkls/model.pkl')['model']
    churn_probability = model.predict_proba(customer_df)[:,1][0]

    response = {'churn_probability': churn_probability, 'created_at': str(datetime.now())}

    prediction_dict = customer_dict | response
    prediction = models.Prediction(**prediction_dict)
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    return response


@app.get("/predictions", response_model=List[schemas.Prediction])
def get_predictions(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    predictions = db.query(models.Prediction).all()

    return predictions



@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()

    return user