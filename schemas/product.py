from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from .category import CategoryResponse


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    image_url: Optional[str] = None

class ProductResponse(ProductBase):
    product_id: int
    date_added: datetime
    is_available: bool
    category: CategoryResponse | None

    class Config:
        orm_mode = True
