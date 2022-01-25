import joblib
import pandas as pd
from pathlib import Path

from fastapi import APIRouter, Depends
from app import models, schemas
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime
from typing import List


router = APIRouter(
    prefix="/predictions",
    tags=["prediction"]
)

BASE_DIR = Path(__file__).parent.parent.parent

@router.post("/", response_model=schemas.CustomerResponse)
def create_prediction(customer: schemas.Customer, db: Session = Depends(get_db)):
    
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


@router.get("/", response_model=List[schemas.Prediction])
def get_predictions(db: Session = Depends(get_db)):
    predictions = db.query(models.Prediction).all()

    return predictions
