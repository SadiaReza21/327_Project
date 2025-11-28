from models.product_model import ProductModel, SearchRequestModel, SearchResponseModel
from typing import List, Optional
import re
import uuid


class ProductSearchError(Exception):
    pass


class DatabaseConnectionError(ProductSearchError):
    pass


class InvalidSearchInputError(ProductSearchError):
    pass


class ProductService:
    
    def __init__(self):
        self.products_database = self.fun_initialize_sample_products()
    
    
    def fun_initialize_sample_products(self) -> List[ProductModel]:
        """
        Initialize sample product data
        """
        return [
            ProductModel(
                name="Fresh Apples",
                price=2.99,
                category="Fruits",
                image_url="/static/images/apples.jpg",
                description="Fresh red apples, perfect for snacking",
                stock_quantity=50
            ),
            ProductModel(
                name="Bananas",
                price=1.49,
                category="Fruits", 
                image_url="/static/images/bananas.jpg",
                description="Sweet yellow bananas, rich in potassium",
                stock_quantity=35
            ),
            ProductModel(
                name="Carrots",
                price=1.99,
                category="Vegetables",
                image_url="/static/images/carrots.jpg",
                description="Fresh organic carrots, great for cooking",
                stock_quantity=40
            ),
            ProductModel(
                name="Milk",
                price=3.49,
                category="Dairy",
                image_url="/static/images/milk.jpg",
                description="Fresh whole milk, 1 gallon",
                stock_quantity=25
            ),
            ProductModel(
                name="Bread",
                price=2.99,
                category="Bakery",
                image_url="/static/images/bread.jpg",
                description="Fresh whole wheat bread",
                stock_quantity=30
            ),
            ProductModel(
                name="Eggs",
                price=4.99,
                category="Dairy",
                image_url="/static/images/eggs.jpg",
                description="Farm fresh eggs, dozen",
                stock_quantity=20
            ),
            ProductModel(
                name="Chicken Breast",
                price=8.99,
                category="Meat",
                image_url="/static/images/chicken.jpg",
                description="Boneless chicken breast, 1lb",
                stock_quantity=15
            ),
            ProductModel(
                name="Rice",
                price=5.99,
                category="Grains",
                image_url="/static/images/rice.jpg",
                description="Long grain white rice, 2lb bag",
                stock_quantity=18
            )
        ]
    
    
    def fun_search_products(self, search_request: SearchRequestModel) -> SearchResponseModel:
        """
        Search products based on search criteria
        """
        try:
            self.fun_validate_search_input(search_request.query)
            
            filtered_products = self.fun_perform_search_operation(
                search_query=search_request.query,
                category_filter=search_request.category,
                min_price_filter=search_request.min_price,
                max_price_filter=search_request.max_price
            )
            
            return SearchResponseModel(
                products=filtered_products,
                total_count=len(filtered_products),
                search_query=search_request.query
            )
            
        except InvalidSearchInputError:
            raise
        except Exception as search_operation_error:
            raise DatabaseConnectionError("Search operation failed") from search_operation_error
    
    
    def fun_get_all_products(self) -> List[ProductModel]:
        """
        Get all available products
        """
        try:
            return [product for product in self.products_database if product.is_available]
        except Exception as fetch_error:
            raise DatabaseConnectionError("Failed to fetch products") from fetch_error
    
    
    def fun_validate_search_input(self, search_query: str):
        """
        Validate search input for security
        """
        INVALID_PATTERNS = [r"<.*?>", r"script", r"--", r";"]
        
        for pattern in INVALID_PATTERNS:
            if re.search(pattern, search_query, re.IGNORECASE):
                raise InvalidSearchInputError("Invalid characters in search query")
    
    
    def fun_perform_search_operation(
        self,
        search_query: str,
        category_filter: Optional[str] = None,
        min_price_filter: Optional[float] = None,
        max_price_filter: Optional[float] = None
    ) -> List[ProductModel]:
        """
        Perform the actual search with filters
        """
        search_terms = search_query.lower().split()
        filtered_results = []
        
        for product in self.products_database:
            if not product.is_available:
                continue
            
            # Search in name and category
            product_match = any(
                term in product.name.lower() or term in product.category.lower() 
                for term in search_terms
            )
            
            if not product_match:
                continue
            
            # Apply category filter
            category_match = (
                category_filter is None or 
                product.category.lower() == category_filter.lower()
            )
            
            # Apply price filter
            price_match = True
            if min_price_filter is not None and product.price < min_price_filter:
                price_match = False
            if max_price_filter is not None and product.price > max_price_filter:
                price_match = False
            
            if category_match and price_match:
                filtered_results.append(product)
        
        return filtered_results
    
    
    def fun_get_categories(self) -> List[str]:
        """
        Get all available product categories
        """
        try:
            categories = set(product.category for product in self.products_database)
            return sorted(list(categories))
        except Exception as category_error:
            raise DatabaseConnectionError("Failed to fetch categories") from category_error