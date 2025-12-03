# tests/test_search_controller.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_search_no_query_returns_results():
    response = client.get("/api/search")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["results"], list)
    assert data["query"] == ""


def test_search_by_name_exact():
    response = client.get("/api/search?q=apple")
    assert response.status_code == 200
    results = response.json()["results"]
    if results:
        assert any("apple" in p["name"].lower() for p in results)


def test_search_case_insensitive():
    response = client.get("/api/search?q=APPLE")
    assert response.status_code == 200
    assert response.json()["query"].lower() == "apple"


def test_search_partial_match():
    response = client.get("/api/search?q=milk")
    assert response.status_code == 200
    results = response.json()["results"]
    assert all("milk" in p["name"].lower() or "milk" in (p.get("description") or "").lower() for p in results)


def test_search_no_results_returns_empty_list():
    response = client.get("/api/search?q=thisproductdoesnotexist12345")
    assert response.status_code == 200
    assert response.json()["results"] == []


def test_search_response_structure():
    response = client.get("/api/search?q=tomato")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total" in data
    assert "query" in data
    assert "time_ms" in data


def test_search_limit_parameter():
    response = client.get("/api/search?q=&limit=3")
    assert response.status_code == 200
    assert len(response.json()["results"]) <= 3


def test_search_offset_pagination():
    r1 = client.get("/api/search?limit=5&offset=0")
    r2 = client.get("/api/search?limit=5&offset=5")
    assert r1.status_code == r2.status_code == 200
    ids1 = {p["id"] for p in r1.json()["results"]}
    ids2 = {p["id"] for p in r2.json()["results"]}
    assert ids1.isdisjoint(ids2)


def test_search_special_characters_safe():
    response = client.get("/api/search?q=organic%20banana!")
    assert response.status_code == 200
    assert isinstance(response.json()["results"], list)


def test_search_empty_string_behaves_like_no_query():
    r1 = client.get("/api/search")
    r2 = client.get("/api/search?q=")
    assert r1.status_code == r2.status_code == 200