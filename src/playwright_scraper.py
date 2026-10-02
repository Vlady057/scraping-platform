from playwright.sync_api import sync_playwright


BASE_URL = "https://www.web-scraping.dev/products"


def get_products_with_playwright():
    products = []
    seen_products = set()
    visited_urls = set()
    urls_to_visit = [BASE_URL]

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            while urls_to_visit:
                url = urls_to_visit.pop(0)

                if url in visited_urls:
                    continue

                visited_urls.add(url)

                page.goto(url, wait_until="domcontentloaded")

                items = page.locator("div.row.product")

                for i in range(items.count()):
                    item = items.nth(i)

                    name = item.locator("h3").inner_text().strip()
                    price = item.locator(".price").inner_text().strip()

                    product_key = (name, price)

                    if product_key not in seen_products:
                        seen_products.add(product_key)

                        products.append(
                            {
                                "name": name,
                                "price": price,
                            }
                        )

                links = page.locator("a")

                for i in range(links.count()):
                    href = links.nth(i).get_attribute("href")

                    if href and "page=" in href:
                        if href.startswith("/"):
                            href = "https://www.web-scraping.dev" + href

                        if (
                            href not in visited_urls
                            and href not in urls_to_visit
                        ):
                            urls_to_visit.append(href)

        finally:
            browser.close()

    return products