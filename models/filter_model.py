from pydantic import BaseModel, Field
from typing import List, Optional
from models.product_model import ProductModel

class FilterRequestModel(BaseModel):
    """
    Filter request model for product filtering
    """
    category: Optional[str] = Field(
        None,
        description="Filter by specific category"
    )
    min_price: Optional[float] = Field(
        None,
        ge=0,
        description="Minimum price filter"
    )
    max_price: Optional[float] = Field(
        None,
        ge=0,
        description="Maximum price filter"
    )

class FilterResponseModel(BaseModel):
    """
    Filter response model
    """
    products: List[ProductModel]  # List of filtered products
    total_count: int  # Total number of products after filtering
    applied_filters: dict  # Dictionary of applied filters

class FilterErrorResponseModel(BaseModel):
    """
    Error response model for filter operations
    """
    error: str  # Error message
    details: Optional[str] = None  # Optional detailed error information