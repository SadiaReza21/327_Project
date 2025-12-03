import json
import pytest
from models.product import Product
from models.archived import Archived
from controllers.archived_controller import sync_archive


with open("tests/archived/test-data/products_archived_add.json", "r") as f:
    archive_add_data = json.load(f)

with open("tests/archived/test-data/products_archived_remove.json", "r") as f:
    archive_remove_data = json.load(f)


@pytest.mark.parametrize("prod", archive_add_data)
def test_sync_archive_addn(db_session, prod):
    db = db_session

    product = Product(
        product_id=prod["product_id"],
        name=prod["name"],
        price=prod["price"],
        stock=prod.get("stock", 0),
        category_id=prod["category_id"],
        is_available=prod.get("is_available", False),
        is_archived=prod.get("is_archived", True),
    )
    db.add(product)
    db.commit()

    sync_archive(db)

    arch = db.query(Archived).filter_by(product_id=prod["product_id"]).first()

    assert arch is not None, f"Product {prod['name']} was not archived"
    assert arch.stock == prod.get("stock", 0)


@pytest.mark.parametrize("prod", archive_remove_data)
def test_sync_archive_removen(db_session, prod):
    db = db_session

    product = Product(
        product_id=prod["product_id"],
        name=prod["name"],
        price=prod["price"],
        stock=prod["current_stock"],
        category_id=prod["category_id"],
        is_available=prod.get("is_available", True),
        is_archived=True,
    )

    archive_entry = Archived(
        product_id=prod["product_id"],
        name=prod["name"],
        stock=prod["existing_stock"],
        is_archived=True,
    )

    db.add_all([product, archive_entry])
    db.commit()

    sync_archive(db)

    arch = db.query(Archived).filter_by(product_id=prod["product_id"]).first()
    if prod["should_be_removed"]:
        assert arch is None, f"Product {prod['name']} should have been removed"
    else:
        assert arch is not None, f"Product {prod['name']} should still exist"
