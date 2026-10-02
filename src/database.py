import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "scraping_platform"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price NUMERIC(10, 2) NOT NULL
        )
        """
    )

    connection.commit()

    cursor.close()
    connection.close()


def save_products(products):
    create_table()

    connection = get_connection()
    cursor = connection.cursor()

    for product in products:
        cursor.execute(
            """
            SELECT id
            FROM products
            WHERE name = %s AND price = %s
            """,
            (
                product["name"],
                product["price"],
            ),
        )

        existing_product = cursor.fetchone()

        if existing_product is None:
            cursor.execute(
                """
                INSERT INTO products (name, price)
                VALUES (%s, %s)
                """,
                (
                    product["name"],
                    product["price"],
                ),
            )

    connection.commit()

    cursor.close()
    connection.close()


def get_products():
    create_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, price
        FROM products
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows