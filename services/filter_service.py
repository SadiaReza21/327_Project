from models.product_model import ProductModel
from models.filter_model import FilterRequestModel, FilterResponseModel
from typing import List, Optional


class FilterError(Exception):
    """
    Base exception for filter operations
    """
    pass


class DatabaseConnectionError(FilterError):
    """
    Raised when database operations fail (e.g., connection lost, query error)
    """
    pass


class InvalidFilterInputError(FilterError):
    """
    Raised when filter parameters are logically invalid (e.g., min_price > max_price)
    """
    pass


class FilterService:
    """
    Service layer for product filtering operations
    Performs server-side filtering by category and price range
    """
    
    def __init__(self, product_service):
        """
        Initialize with a ProductService instance to access product data
        """
        self.product_service = product_service
    
    
    def fun_filter_products(
        self, 
        filter_request: FilterRequestModel
          ) -> FilterResponseModel:
        """
        Filter products based on category and price range
        Returns filtered products with total count and applied filters metadata
        """
        try:
            self.fun_validate_filter_input(filter_request)
            
            all_products = self.product_service.fun_get_all_products()
            filtered_products = self.fun_apply_filters(
                products=all_products,
                category_filter=filter_request.category,
                min_price_filter=filter_request.min_price,
                max_price_filter=filter_request.max_price
            )
            
            applied_filters = {
                "category": filter_request.category,
                "min_price": filter_request.min_price,
                "max_price": filter_request.max_price
            }
            
            return FilterResponseModel(
                products=filtered_products,
                total_count=len(filtered_products),
                applied_filters=applied_filters
            )
            
        except InvalidFilterInputError:
            raise
        except Exception as filter_operation_error:
            raise DatabaseConnectionError(
                "Filter operation failed"
            ) from filter_operation_error
    
    
    def fun_validate_filter_input(self, filter_request: FilterRequestModel):
        """
        Validate filter input parameters
        Ensures min_price is not greater than max_price
        """
        if (filter_request.min_price is not None and 
            filter_request.max_price is not None):
            if filter_request.min_price > filter_request.max_price:
                raise InvalidFilterInputError(
                    "Minimum price cannot be greater than maximum price"
                )
    
    
    def fun_apply_filters(
        self,
        products: List[ProductModel],
        category_filter: Optional[str] = None,
        min_price_filter: Optional[float] = None,
        max_price_filter: Optional[float] = None
    ) -> List[ProductModel]:
        """
        Apply category and price filters to products
        Only includes available products (is_available == True)
        Case-insensitive category matching
        """
        filtered_results = []
        
        for product in products:
            if not product.is_available:
                continue
            
            category_match = (
                category_filter is None or 
                category_filter == "" or
                product.category.lower() == category_filter.lower()
            )
            
            price_match = True
            if min_price_filter is not None:
                if product.price < min_price_filter:
                    price_match = False
            if max_price_filter is not None:
                if product.price > max_price_filter:
                    price_match = False
            
            if category_match and price_match:
                filtered_results.append(product)
        
        return filtered_results
    
    
    def fun_get_categories(self) -> List[str]:
        """
        Get all available product categories
        Delegates to ProductService and wraps errors
        """
        try:
            return self.product_service.fun_get_categories()
        except Exception as category_error:
            raise DatabaseConnectionError(
                "Failed to fetch categories"
            ) from category_error