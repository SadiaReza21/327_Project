from pydantic import BaseModel, Field
from typing import List, Optional
import uuid


class ProductModel(BaseModel):
    product_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    image_url: str
    description: str
    stock_quantity: int = Field(..., ge=0)
    is_available: bool = True


class SearchRequestModel(BaseModel):
    query: str = Field(..., min_length=1, description="Product name or category to search")
    category: Optional[str] = Field(None, description="Filter by specific category")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price filter")



class SearchResponseModel(BaseModel):
    products: List[ProductModel]
    total_count: int
    search_query: str


class ErrorResponseModel(BaseModel):
    error: str
    details: Optional[str] = None