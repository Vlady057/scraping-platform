from fastapi.testclient import TestClient

from src.main import app
from src.database import save_products


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Scraping Platform API is running"
    }


def test_products():
    response = client.get("/products")

    assert response.status_code == 200

    products = response.json()

    assert isinstance(products, list)
    assert len(products) > 0


def test_products_have_required_fields():
    response = client.get("/products")

    assert response.status_code == 200

    products = response.json()

    for product in products:
        assert "name" in product
        assert "price" in product


def test_products_db():
    save_products([
        {"name": "CI Test Product", "price": 19.99},
    ])

    response = client.get("/products/db")

    assert response.status_code == 200

    products = response.json()

    assert isinstance(products, list)
    assert len(products) > 0


def test_products_db_have_ids():
    save_products([
        {"name": "CI Test Product With ID", "price": 29.99},
    ])

    response = client.get("/products/db")

    assert response.status_code == 200

    products = response.json()

    assert isinstance(products, list)
    assert len(products) > 0

    for product in products:
        assert "id" in product
        assert "name" in product
        assert "price" in product