from fastapi import APIRouter, HTTPException, Query
from typing import Optional  # ADD THIS IMPORT
from models.filter_model import (
    FilterRequestModel, 
    FilterResponseModel, 
    FilterErrorResponseModel
)
from services.filter_service import (
    FilterService, 
    InvalidFilterInputError,  # Make sure this is imported
    DatabaseConnectionError
)
from services.product_service import ProductService


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
            ge=0,  # FIXED: Changed g==0 to ge=0
            description="Minimum price filter"
        ),
        max_price: Optional[float] = Query(
            None, 
            ge=0,  # FIXED: Changed g==0 to ge=0
            description="Maximum price filter"
        ),
        search: Optional[str] = Query(
            None,
            description="Search by product name"
        ),
        sort: Optional[str] = Query(
            None,
            description="Sort by: price_low, price_high, name_asc, name_desc"
        )
    ) -> FilterResponseModel:
        """
        Handle product filter requests with enhanced filtering
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
            
            # Apply search filter if provided
            if search:
                filtered_results = [
                    product for product in filter_results.products 
                    if search.lower() in product.name.lower()
                ]
                filter_results.products = filtered_results
                filter_results.total_count = len(filtered_results)
            
            # Apply sorting if requested
            if sort:
                if sort == "price_low":
                    filter_results.products.sort(key=lambda x: x.price)
                elif sort == "price_high":
                    filter_results.products.sort(key=lambda x: x.price, reverse=True)
                elif sort == "name_asc":
                    filter_results.products.sort(key=lambda x: x.name)
                elif sort == "name_desc":
                    filter_results.products.sort(key=lambda x: x.name, reverse=True)
            
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