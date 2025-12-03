from fastapi import APIRouter, Depends
from database.database import get_db
from models.cart import CartItem 
from schemas.cart import CartItemCreate

router = APIRouter(prefix="/carts", tags=["Cart"])

# Get buyer's cart
@router.get("/{buyer_id}")
def get_cart(buyer_id: int, db=Depends(get_db)):
    db.execute("""
        SELECT c.cart_id, c.product_id, p.name AS product_name, c.quantity, p.price
        FROM carts c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.buyer_id=%s
    """, (buyer_id,))
    rows = db.fetchall()

    return [
        CartItem(
            cart_id=row['cart_id'],
            buyer_id=buyer_id,
            product_id=row['product_id'],
            product_name=row['product_name'],
            quantity=row['quantity'],
            price=row['price']
        )
        for row in rows
    ]


# Add product to cart
@router.post("/add")
def add_to_cart(item: CartItemCreate, db=Depends(get_db)):
    db.execute("""
        SELECT quantity FROM carts WHERE buyer_id=%s AND product_id=%s
    """, (item.buyer_id, item.product_id))
    existing = db.fetchone()
    
    if existing:
        new_qty = existing['quantity'] + item.quantity
        db.execute("""
            UPDATE carts SET quantity=%s WHERE buyer_id=%s AND product_id=%s
        """, (new_qty, item.buyer_id, item.product_id))
    else:
        db.execute("""
            INSERT INTO carts (buyer_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (item.buyer_id, item.product_id, item.quantity))
    
    return {"message": "Product added to cart"}


# Remove product
@router.delete("/remove/{cart_id}")
def remove_from_cart(cart_id: int, db=Depends(get_db)):
    db.execute("DELETE FROM carts WHERE cart_id=%s", (cart_id,))
    return {"message": "Cart item removed successfully"}
