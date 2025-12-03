import json
import pytest
from controllers.product_controller import check_product_status
from models.product import Product


with open("tests/product/test-data/products_status.json") as f:
    products_data = json.load(f)


@pytest.mark.parametrize("prod", products_data)
def test_check_product_status(db_session, prod):
    db = db_session

    product = Product(
        product_id=prod["product_id"],
        name=prod["name"],
        stock=prod["stock"],
        price=prod["price"],
        category_id=prod["category_id"],
        is_available=prod["is_available"],
        is_archived=prod["is_archived"],
    )
    db.add(product)
    db.commit()

    check_product_status(db)

    p = db.query(Product).filter_by(product_id=prod["product_id"]).first()
    db.refresh(p)

    assert (
        p.is_available == prod["expected_available"]
    ), f"Availability mismatch for {p.name}. Input: {prod}"
    assert (
        p.is_archived == prod["expected_archived"]
    ), f"Archived status mismatch for {p.name}. Input: {prod}"
