from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from db import SessionLocal, engine
from models import CartItem 
from pydantic import BaseModel

class CartItemRequest(BaseModel):
    product_id: str
    quantity: int

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cart/users/{user_id}")
def add_or_update_cart_item(user_id: str, cart_item: CartItemRequest, db: Session = Depends(get_db)):
    db_item = db.query(CartItem).filter(CartItem.user_id==user_id, CartItem.product_id==cart_item.product_id).first()
    
    if db_item:
        # If the item exists, update the quantity
        db_item.quantity += cart_item.quantity
    else:
        # If the item does not exist, create a new one
        db_item = CartItem(user_id=user_id, product_id=cart_item.product_id, quantity=cart_item.quantity)
        db.add(db_item)
    
    try:
        db.commit()
        db.refresh(db_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return db_item

@app.get("/cart/users/{user_id}")
async def get_cart_items(user_id: str, db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="No cart items found for this user")

    return [{"product_id": item.product_id, "quantity": item.quantity} for item in cart_items]

@app.delete("/cart/users/{user_id}")
async def delete_cart_items(user_id: str, db: Session = Depends(get_db)):
    result = db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    if result == 0:
        raise HTTPException(status_code=404, detail="No cart items found for this user")

    db.commit()
    return {"msg": "All cart items deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)