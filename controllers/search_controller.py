from fastapi import APIRouter, HTTPException, Query
from models.product_model import ProductModel, SearchRequestModel, SearchResponseModel, ErrorResponseModel
from services.product_service import ProductService, InvalidSearchInputError, DatabaseConnectionError
from typing import List, Optional

class SearchController:
    """Controller for product search operations."""
   
    def __init__(self):
        """Initialize the SearchController with router and product service."""
        self.router = APIRouter()
        self.product_service = ProductService()
        self.fun_setup_routes()
   
   
    def fun_setup_routes(self):
        """
        Setup API routes for search functionality
        """
        self.router.add_api_route(
            path="/api/v1/search",
            endpoint=self.fun_handle_search,
            methods=["GET"],
            response_model=SearchResponseModel,
            responses={
                400: {"model": ErrorResponseModel},
                500: {"model": ErrorResponseModel}
            }
        )
       
        self.router.add_api_route(
            path="/api/v1/products",
            endpoint=self.fun_get_all_products,
            methods=["GET"],
            response_model=List[ProductModel]
        )
       
        self.router.add_api_route(
            path="/api/v1/categories",
            endpoint=self.fun_get_categories,
            methods=["GET"],
            response_model=List[str]
        )
   
   
    async def fun_handle_search(
        self,
        query: str = Query(..., min_length=1, description="Product name or category to search"),
        category: Optional[str] = Query(None, description="Filter by specific category"),
        min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
        max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter")
    ) -> SearchResponseModel:
        """
        Handle product search requests
        """
        try:
            # Create search request model from query parameters
            search_request = SearchRequestModel(
                query=query,
                category=category,
                min_price=min_price,
                max_price=max_price
            )
           
            # Perform search using the product service
            search_results = self.product_service.fun_search_products(search_request)
            return search_results
           
        except InvalidSearchInputError as invalid_input_error:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid search input",
                    "details": str(invalid_input_error)
                }
            )
        except DatabaseConnectionError as db_connection_error:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Database unavailable",
                    "details": "Unable to load search results. Please try again later."
                }
            )
        except Exception as unexpected_error:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Search failed",
                    "details": "Please try again later."
                }
            )
   
   
    async def fun_get_all_products(self):
        """
        Get all available products
        """
        try:
            # Retrieve all products from the product service
            products = self.product_service.fun_get_all_products()
            return products
        except DatabaseConnectionError as db_error:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Failed to fetch products",
                    "details": str(db_error)
                }
            )
   
   
    async def fun_get_categories(self):
        """
        Get all available categories
        """
        try:
            # Retrieve categories from the product service
            categories = self.product_service.fun_get_categories()
            return categories
        except DatabaseConnectionError as db_error:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Failed to fetch categories",
                    "details": str(db_error)
                }
            )