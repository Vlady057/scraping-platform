import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.web-scraping.dev/products"


def get_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return BeautifulSoup(response.text, "html.parser")


def parse_products(soup):
    products = []

    for item in soup.select("div.row.product"):
        name = item.select_one("h3")
        price = item.select_one(".price")

        if name and price:
            products.append({
                "name": name.get_text(strip=True),
                "price": price.get_text(strip=True),
            })

    return products


def scrape_products(page=1):
    url = f"{BASE_URL}?page={page}"

    soup = get_page(url)

    return parse_products(soup)


def scrape_all_products():
    all_products = []
    visited_urls = set()
    seen_products = set()

    url = BASE_URL

    while url and url not in visited_urls:
        visited_urls.add(url)

        soup = get_page(url)

        products = parse_products(soup)

        for product in products:
            product_key = (product["name"], product["price"])

            if product_key not in seen_products:
                seen_products.add(product_key)
                all_products.append(product)

        next_url = None

        for link in soup.select("a"):
            if link.get_text(strip=True) == ">" and link.get("href"):
                next_url = link["href"]
                break

        url = next_url

    return all_products