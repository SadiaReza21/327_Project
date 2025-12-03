# tests/test_filter_controller.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_filter_no_params_returns_all():
    response = client.get("/api/filter")
    assert response.status_code == 200
    assert isinstance(response.json()["results"], list)


def test_filter_by_single_category():
    response = client.get("/api/filter?category=Fruits")
    assert response.status_code == 200
    results = response.json()["results"]
    if results:
        assert all(p["category"] == "Fruits" for p in results)


def test_filter_multiple_categories():
    response = client.get("/api/filter?category=Fruits&category=Vegetables")
    assert response.status_code == 200
    cats = {p["category"] for p in response.json()["results"]}
    assert len(cats) >= 1


def test_filter_price_range_min_max():
    response = client.get("/api/filter?min_price=50&max_price=150")
    assert response.status_code == 200
    for p in response.json()["results"]:
        assert 50 <= p["price"] <= 150


def test_filter_price_min_only():
    response = client.get("/api/filter?min_price=200")
    assert response.status_code == 200
    assert all(p["price"] >= 200 for p in response.json()["results"])


def test_filter_price_max_only():
    response = client.get("/api/filter?max_price=100")
    assert response.status_code == 200
    assert all(p["price"] <= 100 for p in response.json()["results"])


def test_filter_in_stock_only():
    response = client.get("/api/filter?in_stock=true")
    assert response.status_code == 200
    assert all(p["in_stock"] for p in response.json()["results"])


def test_filter_sort_price_asc():
    response = client.get("/api/filter?sort=price_asc")
    assert response.status_code == 200
    prices = [p["price"] for p in response.json()["results"]]
    assert prices == sorted(prices)


def test_filter_sort_price_desc():
    response = client.get("/api/filter?sort=price_desc")
    assert response.status_code == 200
    prices = [p["price"] for p in response.json()["results"]]
    assert prices == sorted(prices, reverse=True)


def test_filter_combined_search_and_category():
    response = client.get("/api/filter?q=apple&category=Fruits")
    assert response.status_code == 200
    for p in response.json()["results"]:
        assert "apple" in p["name"].lower()
        assert p["category"] == "Fruits"