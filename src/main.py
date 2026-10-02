from fastapi import FastAPI
from src.scraper import scrape_products, scrape_all_products
from src.database import save_products, get_products


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Scraping Platform API is running"}


@app.get("/products")
def get_products_api(page: int = 1):
    return scrape_products(page)


@app.get("/products/all")
def get_all_products():
    products = scrape_all_products()

    save_products(products)

    return products


@app.get("/products/db")
def get_products_from_db():
    rows = get_products()

    return [
        {
            "id": row[0],
            "name": row[1],
            "price": float(row[2]),
        }
        for row in rows
    ]