from src.scraper import scrape_products, parse_products
from bs4 import BeautifulSoup


def test_scrape_products_returns_list():
    products = scrape_products(1)

    assert isinstance(products, list)


def test_scrape_products_returns_products():
    products = scrape_products(1)

    assert len(products) > 0


def test_product_has_required_fields():
    products = scrape_products(1)

    for product in products:
        assert "name" in product
        assert "price" in product


def test_parse_products():
    html = """
    <div class="row product">
        <h3>Test Product</h3>
        <div class="price">19.99</div>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")

    products = parse_products(soup)

    assert products == [
        {
            "name": "Test Product",
            "price": "19.99",
        }
    ]