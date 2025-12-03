import json
import pytest
from models.product import Product
from models.inventory import Inventory
from controllers.inventory_controller import sync_inventory

with open("tests/inventory/test-data/products_inventory_add.json") as f:
    products_add = json.load(f)

with open("tests/inventory/test-data/products_inventory_update.json") as f:
    products_update = json.load(f)

with open("tests/inventory/test-data/products_inventory_remove.json") as f:
    products_remove = json.load(f)


@pytest.mark.parametrize("prod", products_add)
def test_inventory_adds_item(db_session, prod):
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

    sync_inventory(db)

    inv = db.query(Inventory).filter_by(product_id=prod["product_id"]).first()

    if prod["is_available"] and prod["initial_stock"] > 0:
        assert inv is not None, f"{prod['name']} not added to inventory. Input: {prod}"
        assert inv.stock == prod["expected_stock"], (
            f"Inventory stock mismatch for {prod['name']}. "
            f"Expected {prod['expected_stock']}, got {inv.stock}. Input: {prod}"
        )
    else:
        assert (
            inv is None
        ), f"{prod['name']} should not exist in inventory. Input: {prod}"


@pytest.mark.parametrize("prod", products_update)
def test_inventory_updates_stock(db_session, prod):
    db = db_session

    product = Product(
        product_id=prod["product_id"],
        name=prod["name"],
        stock=prod["current_stock"],
        price=prod["price"],
        category_id=prod["category_id"],
        is_available=prod["is_available"],
        is_archived=prod["is_archived"],
    )

    inv = Inventory(
        product_id=prod["product_id"],
        name=prod["name"],
        stock=prod["existing_stock"],
        is_available=prod["is_available"],
    )
    db.add_all([product, inv])
    db.commit()

    sync_inventory(db)

    inv = db.query(Inventory).filter_by(product_id=prod["product_id"]).first()
    if inv is not None:
        assert inv.stock == prod["expected_stock"], (
            f"Inventory stock mismatch for {prod['name']}. "
            f"Expected {prod['expected_stock']}, got {inv.stock}. Input: {prod}"
        )


@pytest.mark.parametrize("prod", products_remove)
def test_inventory_removes_item(db_session, prod):
    db = db_session

    product = Product(
        product_id=prod["product_id"],
        name=prod["name"],
        stock=prod["current_stock"],
        price=prod["price"],
        category_id=prod["category_id"],
        is_available=prod["is_available"],
        is_archived=prod["is_archived"],
    )

    inv = Inventory(
        product_id=prod["product_id"],
        name=prod["name"],
        stock=prod["existing_stock"],
        is_available=prod["is_available"],
    )
    db.add_all([product, inv])
    db.commit()

    sync_inventory(db)

    inv = db.query(Inventory).filter_by(product_id=prod["product_id"]).first()
    if prod["should_be_removed"]:
        assert (
            inv is None
        ), f"Inventory for {prod['name']} should have been removed. Input: {prod}"
    else:
        assert (
            inv is not None
        ), f"Inventory for {prod['name']} should not be removed. Input: {prod}"
        assert inv.stock == prod["expected_stock"], (
            f"Inventory stock mismatch for {prod['name']}. "
            f"Expected {prod['expected_stock']}, got {inv.stock}. Input: {prod}"
        )
