# tests/test_product_model.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.product import Product
import pytest


def test_product_creation_valid():
    p = Product(id=1, name="Apple", price=50.0, category="Fruits")
    assert p.id == 1
    assert p.name == "Apple"
    assert p.price == 50.0
    assert p.category == "Fruits"
    assert p.in_stock is True


def test_product_price_must_be_positive():
    with pytest.raises(ValueError):
        Product(id=1, name="Banana", price=-10, category="Fruits")


def test_product_price_zero_not_allowed():
    with pytest.raises(ValueError):
        Product(id=1, name="Free Item", price=0, category="Test")


def test_product_name_cannot_be_empty():
    with pytest.raises(ValueError):
        Product(id=1, name="", price=30, category="Fruits")


def test_product_rating_must_be_between_0_and_5():
    p = Product(id=3, name="Orange", price=60, category="Fruits", rating=4.5)
    assert p.rating == 4.5

    with pytest.raises(ValueError):
        Product(id=4, name="Bad", price=10, category="Test", rating=6)

    with pytest.raises(ValueError):
        Product(id=5, name="Negative", price=10, category="Test", rating=-1)


def test_product_stock_quantity_can_be_zero():
    p = Product(id=6, name="Out of Stock", price=100, category="Meat", stock_quantity=0)
    assert p.stock_quantity == 0


def test_product_out_of_stock_flag():
    p = Product(id=7, name="Sold Out", price=999, category="Electronics", in_stock=False)
    assert p.in_stock is False


def test_product_json_serialization():
    p = Product(
        id=8,
        name="Premium Mango",
        price=299.99,
        category="Fruits",
        description="Alphonso Mango",
        rating=5.0,
        image_url="https://example.com/mango.jpg"
    )
    json_dict = p.model_dump()
    assert json_dict["price"] == 299.99
    assert json_dict["rating"] == 5.0
    assert json_dict["description"] == "Alphonso Mango"


def test_product_partial_data():
    p = Product(id=10, name="Carrot", price=35.5, category="Vegetables")
    assert p.description is None
    assert p.image_url is None
    assert p.rating is None
    assert p.stock_quantity is None
    assert p.in_stock is True