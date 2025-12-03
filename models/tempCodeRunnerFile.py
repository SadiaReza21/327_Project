from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class ProductModel(BaseModel):
    """Model representing a product."""
    product_id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # Unique product identifier
    name: str = Field(..., min_length=1, max_length=100)  # Product name
    price: float = Field(..., gt=0)  # Product price, must be greater than 0
    category: str = Field(..., min_length=1, max_length=50)  # Product category
    image_url: str  # URL to product image
    description: str  # Product description
    stock_quantity: int = Field(..., ge=0)  # Available stock, non-negative
    is_available: bool = True  # Availability status

class SearchRequestModel(BaseModel):
    """Model for search request parameters."""
    query: str = Field(..., min_length=1, description="Product name or category to search")  # Search query string
    category: Optional[str] = Field(None, description="Filter by specific category")  # Optional category filter
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price filter")  # Optional min price
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price filter")  # Optional max price

class SearchResponseModel(BaseModel):
    """Model for search response."""
    products: List[ProductModel]  # List of search result products
    total_count: int  # Total number of results
    search_query: str  # The original search query

class ErrorResponseModel(BaseModel):
    """Model for error responses."""
    error: str  # Error message
    details: Optional[str] = None  # Optional details