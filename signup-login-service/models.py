# model.py

from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


#CREATE TABLE IF NOT EXISTS "users" (
#  "id" varchar(100),
#  "email" varchar(50),
#  "first_name" TEXT,
#  "last_name" TEXT,
#  PRIMARY KEY ("id", "email")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    