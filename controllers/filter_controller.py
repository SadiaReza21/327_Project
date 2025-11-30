from fastapi import APIRouter, HTTPException, Query
from models.filter_model import (
    FilterRequestModel, 
    FilterResponseModel, 
    FilterErrorResponseModel
)
from services.filter_service import (
    FilterService, 
    InvalidFilterInputError, 
    DatabaseConnectionError
)
from services.product_service import ProductService
from typing import Optional


class FilterController:
    """
    Controller for product filtering operations
    """
    
    def __init__(self):
        self.router = APIRouter()
        product_service = ProductService()
        self.filter_service = FilterService(product_service)
        self.fun_setup_routes()
    
    
    def fun_setup_routes(self):
        """
        Setup API routes for filter functionality
        """
        self.router.add_api_route(
            path="/api/v1/filter",
            endpoint=self.fun_handle_filter,
            methods=["GET"],
            response_model=FilterResponseModel,
            responses={
                400: {"model": FilterErrorResponseModel},
                500: {"model": FilterErrorResponseModel}
            }
        )
        
        self.router.add_api_route(
            path="/api/v1/filter/categories",
            endpoint=self.fun_get_categories,
            methods=["GET"],
            response_model=list
        )
    
    
    async def fun_handle_filter(
        self,
        category: Optional[str] = Query(
            None, 
            description="Filter by specific category"
        ),
        min_price: Optional[float] = Query(
            None, 
            ge=0, 
            description="Minimum price filter"
        ),
        max_price: Optional[float] = Query(
            None, 
            ge=0, 
            description="Maximum price filter"
        )
    ) -> FilterResponseModel:
        """
        Handle product filter requests
        """
        try:
            filter_request = FilterRequestModel(
                category=category,
                min_price=min_price,
                max_price=max_price
            )
            
            filter_results = self.filter_service.fun_filter_products(
                filter_request
            )
            return filter_results
            
        except InvalidFilterInputError as invalid_input_error:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid filter input", 
                    "details": str(invalid_input_error)
                }
            )
        except DatabaseConnectionError as db_connection_error:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Database unavailable", 
                    "details": "Unable to load filter results. Please try again later."
                }
            )
        except Exception as unexpected_error:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Filter failed", 
                    "details": "Please try again later."
                }
            )
    
    
    async def fun_get_categories(self):
        """
        Get all available categories for filtering
        """
        try:
            categories = self.filter_service.fun_get_categories()
            return categories
        except DatabaseConnectionError as db_error:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Failed to fetch categories", 
                    "details": str(db_error)
                }
            )