from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from db import SessionLocal, engine
from models import User

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request and response bodies
class UserCreate(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: str
    first_name: str

# Signup endpoint
@app.post("/signup", response_model=int)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.id == user_data.id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists. Please login.")

    # Create a new user
    new_user = User(id=user_data.id, email=user_data.email, first_name=user_data.first_name, last_name=user_data.last_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Signup successful", "user_id": new_user.id}

# Login endpoint
@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Check if the user exists
    existing_user = db.query(User).filter(User.email == user_data.email, User.first_name == user_data.first_name).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User does not exist. Please sign up.")

    return {"message": "Login successful", "user_id": existing_user.id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)