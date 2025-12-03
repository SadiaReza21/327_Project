from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from controllers.cart_controller import router as cart_controller
from controllers.order_controller import router as order_controller
from controllers.cart_controller import get_cart
from database.database import get_db


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

app.include_router(cart_controller)
app.include_router(order_controller)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/cart_page/{buyer_id}")
def cart_page(request: Request, buyer_id: int, db=Depends(get_db)):
    cart_items = get_cart(buyer_id, db)  
    total = sum(item.total for item in cart_items)
    return templates.TemplateResponse(
        "cart.html",
        {
            "request": request,
            "cart_items": cart_items,
            "total": total,
            "buyer_id": buyer_id,
        },
    )


@app.get("/order/{buyer_id}")
def checkout_page(request: Request, buyer_id: int, db=Depends(get_db)):
    """
    Render the checkout page for a buyer.
    """

    db.execute(
    """
    SELECT c.cart_id, c.quantity, p.name AS product_name, p.price, (c.quantity * p.price) AS total
    FROM carts c
    JOIN products p ON c.product_id = p.product_id
    WHERE c.buyer_id = %s
    """,
        (buyer_id,),
    )

    cart_items = db.fetchall()

    # Calculate total amount
    total = sum(item["total"] for item in cart_items) if cart_items else 0

    return templates.TemplateResponse(
        "checkout.html",
        {
            "request": request,
            "buyer_id": buyer_id,
            "cart_items": cart_items,
            "total": total,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8004, reload=True)
