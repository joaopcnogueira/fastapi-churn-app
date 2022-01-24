from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, null
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Prediction(Base):
    __tablename__ = "predictions"

    id                 = Column(Integer, primary_key=True, nullable=False)
    uf                 = Column(String, nullable=False)
    tot_orders_12m     = Column(Numeric, nullable=False)
    tot_items_12m      = Column(Numeric, nullable=False)
    tot_items_dist_12m = Column(Numeric, nullable=False)
    receita_12m        = Column(Numeric, nullable=False)
    recencia           = Column(Integer, nullable=False)
    churn_probability  = Column(Numeric, nullable=False)
    created_at         = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__ = "users"

    id   = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
