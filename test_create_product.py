from Model.product_class import Product
from database_connection import get_db_connection
from unittest.mock import MagicMock
import pytest


@pytest.mark.parametrize("test_product", [
    Product(124,5,"Cucumber", 
        "Absolutely fresh 40 gm cucumber", 45.50, 40, 
        "ProductImages/124/124.jpg", "2025-12-03", True, False ),   # Every valid value
    Product(124,5,"Cucumber", "", 45.50, 40, 
        "ProductImages/124/124.jpg", "2025-12-03", True, False )    # Empty description (optional), still valid
])
def test_create_product_success(mocker, test_product):
    
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.is_connected.return_value = True

    mocker.patch(
        "Model.product_class.get_db_connection",
        return_value=mock_conn
    )

    result = Product.create_product(test_product)

    assert result is True
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

    # Reseting mocks for the next product
    mock_cursor.reset_mock()
    mock_conn.reset_mock()


@pytest.mark.parametrize("test_product", [
    Product(None,5,"Cucumber", "Short description", 45.50, 
        40, "ProductImages/124/124.jpg", "2025-12-03", True, False ),   # No product id
    Product(124,5,"", "Short description", 45.50, 40, 
        "ProductImages/124/124.jpg", "2025-12-03", True, False ),   # No product name
    Product(124,5,"Cucumber", "Short description", 45.50, None,  
        "ProductImages/124/124.jpg", "2025-12-03", True, False ),   # No stock quantity
    Product(124,5,"Cucumber", "Short description", None, 40, 
        "ProductImages/124/124.jpg", "2025-12-03", True, False ),   # No price
    Product(124,None,"Cucumber", "Short description", 45.50, 40, 
        "ProductImages/124/124.jpg", "2025-12-03", True, False ),   # No category id
    Product(None,5,"Cucumber", "Short description", 45.50, 40, 
        "", "2025-12-03", True, False ),    # No image url
    Product(None,5,"Cucumber", "Short description", 45.50, 40, 
        "", "2025-12-03", True, False ),    # No product id & no image url
    Product(None,None,"", "Short description", None, None, 
        "", "2025-12-03", True, False ),    # All error raising values  
])
def test_create_product_failure(mocker, test_product):
    
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.is_connected.return_value = True

    mocker.patch(
        "Model.product_class.get_db_connection",
        return_value=mock_conn
    )
    
    with pytest.raises(ValueError, match="Required information is not filled!"):
        Product.create_product(test_product)

    # Reseting mocks for the next product
    mock_cursor.reset_mock()
    mock_conn.reset_mock()
