
# Scraping Platform

[![CI](https://github.com/Vlady057/scraping-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/Vlady057/scraping-platform/actions/workflows/ci.yml)

A Python web scraping platform that collects product data from a multi-page website, stores the results in PostgreSQL, and exposes the data through a FastAPI REST API.

The project also includes Selenium and Playwright implementations, automated tests with Pytest, and Docker Compose for running the application and database in isolated containers.

## Features

- Scrape product data using Requests and BeautifulSoup
- Collect products from multiple pages
- Remove duplicate products
- Store scraped data in PostgreSQL
- Automatically create the `products` table
- Expose scraped data through FastAPI
- Retrieve products directly from PostgreSQL
- Selenium scraper implementation
- Playwright scraper implementation
- Automated tests with Pytest
- Continuous Integration with GitHub Actions
- Dockerized FastAPI application
- Dockerized PostgreSQL database
- Environment-based database configuration

## Architecture

```text
Web Scraping
     │
     ▼
Requests / BeautifulSoup
     │
     ▼
Data Processing
     │
     ▼
PostgreSQL
     │
     ▼
FastAPI
     │
     ▼
JSON
```

Additional browser automation implementations:

```text
Selenium ────────┐
                 │
Playwright ──────┤
                 ▼
          Product Extraction
```

## Technologies

| Technology     | Purpose                      |
| -------------- | ---------------------------- |
| Python 3.13    | Main programming language    |
| Requests       | HTTP requests                |
| BeautifulSoup  | HTML parsing                 |
| FastAPI        | REST API                     |
| PostgreSQL     | Database                     |
| psycopg2       | PostgreSQL connection        |
| Selenium       | Browser automation           |
| Playwright     | Browser automation           |
| Pytest         | Automated testing            |
| GitHub Actions | Continuous Integration       |
| Docker         | Application containerization |
| Docker Compose | Multi-container environment  |
| python-dotenv  | Environment variables        |
| Git            | Version control              |

## Project Structure

```text
scraping-platform/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── playwright_scraper.py
│   ├── scraper.py
│   └── selenium_scraper.py
│
├── tests/
│   ├── test_api.py
│   └── test_scraper.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Vlady057/scraping-platform.git
cd scraping-platform
```

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright Chromium:

```bash
playwright install chromium
```

## Environment Variables

Create a `.env` file in the project root:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=scraping_platform
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD
```

The `.env` file is excluded from Git using `.gitignore`.

For Docker, database environment variables are configured in `docker-compose.yml`.

## Running with Docker

Make sure Docker Desktop is running.

Build and start the containers:

```bash
docker compose up --build -d
```

The project starts two containers:

```text
scraping_platform_api
scraping_platform_db
```

The API is available at:

```text
http://localhost:8000
```

The PostgreSQL container is available from the host through port `5433`.

Check running containers:

```bash
docker ps
```

Stop the containers:

```bash
docker compose down
```

To remove the PostgreSQL Docker volume as well:

```bash
docker compose down -v
```

**Warning:** `docker compose down -v` deletes the database volume and its stored data.

## API Endpoints

### Health Check

```http
GET /
```

Example response:

```json
{
    "message": "Scraping Platform API is running"
}
```

### Scrape One Page

```http
GET /products?page=1
```

Returns products from the specified page.

Example response:

```json
[
    {
        "name": "Box of Chocolate Candy",
        "price": "24.99"
    }
]
```

### Scrape All Products

```http
GET /products/all
```

Scrapes all available product pages and saves the results to PostgreSQL.

Example response:

```json
[
    {
        "name": "Box of Chocolate Candy",
        "price": "24.99"
    },
    {
        "name": "Dark Red Energy Potion",
        "price": "4.99"
    }
]
```

### Get Products from Database

```http
GET /products/db
```

Returns products stored in PostgreSQL.

Example response:

```json
[
    {
        "id": 1,
        "name": "Box of Chocolate Candy",
        "price": 24.99
    }
]
```

## Selenium

The project contains a separate Selenium implementation:

```text
src/selenium_scraper.py
```

The scraper:

- Launches Chrome in headless mode
- Navigates through product pages
- Extracts product names and prices
- Handles pagination
- Prevents duplicate products
- Closes the browser after scraping

The Selenium implementation currently extracts 12 unique products.

## Playwright

The Playwright implementation is located in:

```text
src/playwright_scraper.py
```

It:

- Launches Chromium in headless mode
- Navigates through product pages
- Extracts product information
- Handles pagination
- Removes duplicate products
- Closes the browser after scraping

The Playwright implementation currently extracts 12 unique products.

## Database

The application uses PostgreSQL with the following table:

```text
products
├── id
├── name
└── price
```

The table is created automatically with:

```sql
CREATE TABLE IF NOT EXISTS products
```

This allows the Docker environment to start with a clean database without manually creating the table.

The application also prevents duplicate products from being inserted.

## Testing

The project uses Pytest for automated testing.

Run all tests:

```bash
pytest -v
```

Current test suite:

```text
9 passed
```

The tests cover:

- API health check
- Product endpoint
- Product response structure
- Database endpoint
- Database product IDs
- Scraper return type
- Scraper results
- Required product fields
- HTML parser

## Continuous Integration (CI)

The project uses GitHub Actions to run automated tests on every push and pull request to the repository.

The workflow is defined in:

```text
.github/workflows/ci.yml
```

The CI pipeline:

- Sets up Python 3.13
- Starts a PostgreSQL 16 service container
- Installs project dependencies
- Runs the automated test suite with Pytest
- Reports the test results in GitHub Actions

The current CI workflow has passed all 9 tests.

View workflow runs: [GitHub Actions](https://github.com/Vlady057/scraping-platform/actions/workflows/ci.yml)

## Docker Architecture

```text
┌──────────────────────────────┐
│       FastAPI Container      │
│                              │
│  scraper → database → API    │
│                              │
│         Port 8000            │
└──────────────┬───────────────┘
               │
               │ Docker Network
               ▼
┌──────────────────────────────┐
│     PostgreSQL Container     │
│                              │
│          Database            │
│      scraping_platform       │
│                              │
│         Port 5432            │
└──────────────────────────────┘
```

The PostgreSQL data is stored in a Docker named volume.

## Running the API Locally

The API can also be started without Docker.

Make sure PostgreSQL is running and the `.env` file is configured.

Start FastAPI:

```bash
uvicorn src.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

## Scraping Workflow

The main scraping workflow is:

```text
Website
   │
   ▼
Requests
   │
   ▼
BeautifulSoup
   │
   ▼
Product Parsing
   │
   ▼
Duplicate Removal
   │
   ▼
PostgreSQL
   │
   ▼
FastAPI
   │
   ▼
JSON Response
```

Selenium and Playwright provide alternative browser-based implementations for product extraction.

## Example Data

The scraper currently collects 12 unique products from the target website.

Example:

```json
[
    {
        "name": "Box of Chocolate Candy",
        "price": "24.99"
    },
    {
        "name": "Dark Red Energy Potion",
        "price": "4.99"
    },
    {
        "name": "Teal Energy Potion",
        "price": "4.99"
    }
]
```
