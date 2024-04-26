from fastapi import FastAPI, Depends,  HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from db import SessionLocal, engine
import httpx
import uuid
import os
from models import Order


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/checkout")
async def checkout(data: dict, db: Session = Depends(get_db)):

    print("begin checkout")
    # Extract user_id from the request data
    user_id = data.get("user_id")
    email = data.get("email")

    # Make sure user_id is present in the request
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required in the request.")

    # Get the Cart Service URL from the environment variable
    cart_service_url = os.environ.get("CART_SERVICE_URL")
    if not cart_service_url:
        raise HTTPException(status_code=500, detail="Cart Service URL not configured.")
    
    # Make an HTTP request to the cart service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{cart_service_url}/cart/users/{user_id}")

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            cart_data = response.json()
            print(cart_data)
        else:
            # Raise an exception if the request was not successful
            raise HTTPException(status_code=response.status_code, detail=f"Failed to retrieve cart data: {response.text}")
    except httpx.HTTPError as e:
        # Handle HTTP errors
        raise HTTPException(status_code=500, detail=f"HTTP error during cart service request: {str(e)}")
    
    # Extract product_id from the cart data (assuming the structure is consistent)
    product_ids = [item["product_id"] for item in cart_data]

    print(product_ids)

    # Make HTTP request to product catalog service for each product_id
    product_details = []
    #product_catalog_service_url = "http://localhost:8090/products/read?id={}"

    # Get the Product Catalog Service URL from the environment variable
    product_catalog_url = os.environ.get("PRODUCT_CATALOG_URL")
    if not product_catalog_url:
        raise HTTPException(status_code=500, detail="Product Catalog Service URL not configured.")

    try:
        async with httpx.AsyncClient() as client:
            for product_id in product_ids:
                response = await client.get(f"{product_catalog_url}/products/read?id={product_id}")
                if response.status_code == 200:
                    product_details.append(response.json())
                else:
                    # Handle error for product catalog service
                    raise HTTPException(status_code=response.status_code, detail=f"Failed to retrieve product details: {response.text}")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"HTTP error during product catalog service request: {str(e)}")

    # Calculate total price
    total_price = sum(product["price"] for product in product_details)

    # Generate a unique order ID
    order_id = str(uuid.uuid4())

    db_item = Order(order_id=order_id, email= email, amount=total_price)
    db.add(db_item)
    
    try:
        db.commit()
        db.refresh(db_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return db_item

    #return {"order_id": order_id, "total_price": total_price, "products": product_details}
    
 

# Sample request to the checkout service
# You can use any HTTP client to send this request (e.g., curl, Postman, etc.)
# Here, I'll use httpx for demonstration purposes
import httpx

checkout_data = {
    "user_id": "abcde",
    "address": {
        "street_address": "1600 Amp street",
        "city": "Mountain View",
        "state": "CA",
        "country": "USA",
        "zip_code": "94043"
    },
    "email": "someone@example.com",
    "credit_card": {
        "credit_card_number": "4432-8015-6251-0454",
        "credit_card_cvv": 672,
        "credit_card_expiration_year": 24,
        "credit_card_expiration_month": 1
    }
}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)
