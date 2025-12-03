from pydantic import BaseModel

class CheckoutRequest(BaseModel):
    buyer_id: int
    delivery_address: str
