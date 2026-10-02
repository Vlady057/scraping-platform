from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


BASE_URL = "https://www.web-scraping.dev/products"


def get_products_with_selenium():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    products = []
    visited_urls = set()
    seen_products = set()
    urls_to_visit = [BASE_URL]

    try:
        while urls_to_visit:
            url = urls_to_visit.pop(0)

            if url in visited_urls:
                continue

            visited_urls.add(url)

            driver.get(url)

            items = driver.find_elements(
                By.CSS_SELECTOR,
                "div.row.product"
            )

            for item in items:
                name = item.find_element(
                    By.CSS_SELECTOR,
                    "h3"
                ).text.strip()

                price = item.find_element(
                    By.CSS_SELECTOR,
                    ".price"
                ).text.strip()

                product_key = (name, price)

                if product_key not in seen_products:
                    seen_products.add(product_key)

                    products.append(
                        {
                            "name": name,
                            "price": price,
                        }
                    )

            links = driver.find_elements(By.CSS_SELECTOR, "a")

            for link in links:
                href = link.get_attribute("href")

                if href and "page=" in href:
                    if href not in visited_urls and href not in urls_to_visit:
                        urls_to_visit.append(href)

    finally:
        driver.quit()

    return products