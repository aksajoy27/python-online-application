# model.py

from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


#CREATE TABLE IF NOT EXISTS "order" (
#  "order_id" varchar(20),
#  "email" varchar(50),
 # "amount" float,
#  PRIMARY KEY ("order_id")

class Order(Base):
    __tablename__ = 'order'
    
    order_id = Column(String, primary_key=True, index=True)
    email = Column(String)
    amount = Column(Float)
    