from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db
from schemas.order import CheckoutRequest

router = APIRouter(prefix="/order", tags=["order"])


@router.post("/")
def order_confirm(request: CheckoutRequest, db=Depends(get_db)):
    buyer_id = request.buyer_id
    delivery_address = request.delivery_address

    db.execute("""
        SELECT c.cart_id, c.product_id, c.quantity, p.price, p.stock
        FROM carts c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.buyer_id = %s
    """, (buyer_id,))
    cart_items = db.fetchall()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty.")

    for item in cart_items:
        if item['quantity'] > item['stock']:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product ID {item['product_id']}")

        total = item['quantity'] * item['price']

        db.execute("""
            INSERT INTO orders (buyer_id, product_id, quantity, total_amount, status, delivery_address)
            VALUES (%s, %s, %s, %s, 'Confirmed', %s)
        """, (buyer_id, item['product_id'], item['quantity'], total, delivery_address))

        db.execute("""
            UPDATE products
            SET stock = stock - %s
            WHERE product_id = %s
        """, (item['quantity'], item['product_id']))

    db.execute("DELETE FROM carts WHERE buyer_id = %s", (buyer_id,))

    return {"message": "Checkout successful!"}
