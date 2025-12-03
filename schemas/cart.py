from pydantic import BaseModel
class CartItemCreate(BaseModel):
    buyer_id: int
    product_id: int
    quantity: int 

class CartItemUpdate(BaseModel):
    quantity: int