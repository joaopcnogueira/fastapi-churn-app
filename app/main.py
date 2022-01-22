import joblib
import pandas as pd
from pathlib import Path

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from . import models, schemas
from .database import engine, get_db


BASE_DIR = Path('.')
models.Base.metadata.create_all(bind=engine)



app = FastAPI()


@app.post("/predict", response_model=schemas.CustomerResponse)
def predict(customer: schemas.Customer, db: Session = Depends(get_db)):
    
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
def get_predictions(db: Session = Depends(get_db)):
    predictions = db.query(models.Prediction).all()

    return predictions
