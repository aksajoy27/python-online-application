# models.py

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class CartItem(Base):
    __tablename__ = 'cart_items'
    user_id = Column(String, primary_key=True, index=True)
    product_id = Column(String, primary_key=True, index=True)
    quantity = Column(Integer)

