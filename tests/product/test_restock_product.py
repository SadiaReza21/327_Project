import json
import pytest
from fastapi import HTTPException
from models.product import Product
from controllers.inventory_controller import restock_product

with open("tests/product/test-data/products_restock.json") as f:
    products_data = json.load(f)


@pytest.mark.parametrize("prod", products_data)
def test_restock_product_param(db_session, prod):
    db = db_session

    product = Product(
        product_id=prod["product_id"],
        name=prod["name"],
        stock=prod["initial_stock"],
        price=prod["price"],
        category_id=prod["category_id"],
        is_available=prod["is_available"],
        is_archived=prod["is_archived"],
    )
    db.add(product)
    db.commit()

    try:
        updated = restock_product(
            db, product_id=prod["product_id"], additional_stock=prod["additional_stock"]
        )
        db.refresh(updated)

        if prod["expected_success"]:
            assert updated.stock == prod["expected_stock"], (
                f"Product {prod['name']} stock mismatch. "
                f"Expected {prod['expected_stock']}, got {updated.stock}. Input: {prod}"
            )
        else:
            assert (
                False
            ), f"Restocking {prod['name']} should have failed but succeeded. Input: {prod}"

    except HTTPException as e:
        if not prod["expected_success"]:
            assert (
                e.status_code == 400
            ), f"Product {prod['name']} raised unexpected HTTP status {e.status_code}. Input: {prod}"
        else:
            assert (
                False
            ), f"Restocking {prod['name']} failed unexpectedly. Input: {prod}"
