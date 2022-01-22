from pydantic import BaseModel
from datetime import datetime

class Customer(BaseModel):
    uf: str
    tot_orders_12m: float
    tot_items_12m: float
    tot_items_dist_12m: float
    receita_12m: float
    recencia: int


class CustomerResponse(BaseModel):
    churn_probability: float
    created_at: datetime


class Prediction(BaseModel):
    id: int
    uf: str
    tot_orders_12m: float
    tot_items_12m: float
    tot_items_dist_12m: float
    receita_12m: float
    recencia: int
    churn_probability: float
    created_at: datetime

    class Config:
        orm_mode = True
