
from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    
    in_stock: bool = True
    image_url: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    stock_quantity: Optional[int] = Field(default=None, ge=0)

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            float: lambda v: round(v, 2) if v is not None else None
        }
    }