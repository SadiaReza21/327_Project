
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_filter_no_params_returns_all():
    response = client.get("/api/v1/filter")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["products"], list)
    assert "total_count" in data


def test_filter_by_single_category():
    response = client.get("/api/v1/filter?category=Fruits")
    assert response.status_code == 200
    results = response.json()["products"]
    if results:
        assert all(p["category"] == "Fruits" for p in results)




def test_filter_price_range_min_max():
    response = client.get("/api/v1/filter?min_price=1&max_price=5")
    assert response.status_code == 200
    for p in response.json()["products"]:
        assert 1 <= p["price"] <= 5


def test_filter_price_min_only():
    response = client.get("/api/v1/filter?min_price=3")
    assert response.status_code == 200
    for p in response.json()["products"]:
        assert p["price"] >= 3


def test_filter_price_max_only():
    response = client.get("/api/v1/filter?max_price=5")
    assert response.status_code == 200
    for p in response.json()["products"]:
        assert p["price"] <= 5



def test_filter_sort_price_asc():
    response = client.get("/api/v1/filter?sort=price_low")
    assert response.status_code == 200
    prices = [p["price"] for p in response.json()["products"]]
    assert prices == sorted(prices)


