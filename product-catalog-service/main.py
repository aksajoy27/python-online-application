from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from db import SessionLocal, engine
from models import Products 


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products/read")
async def read_product(id: str, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/products/search")
async def search_products(desc: str = Query(..., min_length=3), db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.description.like(f"%{desc}%")).all()
    return products

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)