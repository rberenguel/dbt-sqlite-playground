import sqlite3
import os
import logging
import random

from sqlite3 import Cursor

from colorlog import ColoredFormatter

logger = logging.getLogger("dbt-playground")


def configure_logger():
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "yellow",
            "INFO": "cyan",
            "WARNING": "purple",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


PLAYGROUND = "playground.sqlite3"
PRODUCTS = {
    "potato": 12,
    "book": 42,
}
ORDERS = 10


def clean():
    try:
        os.remove(PLAYGROUND)
        logger.info("Database purged")
    except FileNotFoundError:
        logger.info("No database to purge")


def add_products(cursor: Cursor):

    cursor.execute("""CREATE TABLE products (id int, name text, price int)""")
    logger.info("Products table created")
    for product_id, (product, price) in enumerate(PRODUCTS.items()):
        cursor.execute(
            f"INSERT INTO products VALUES ({product_id}, '{product}', {price})"
        )
    logger.info("Products table populated")


def generate_orders_and_invoices(cursor: Cursor):
    cursor.execute("""CREATE TABLE orders (id int, product_id int, qty int)""")
    logger.info("Orders table created")
    cursor.execute("""CREATE TABLE invoices (id int, order_id int, status text)""")
    logger.info("Invoices table created")
    paid = 0
    total = 0
    for order_id in range(0, ORDERS):
        cost = 0
        for product_id, (product, price) in enumerate(PRODUCTS.items()):
            qty = random.randrange(1, 5)
            cost += qty * price  # I'm not using this for anything though
            cursor.execute(
                f"INSERT INTO orders VALUES ({order_id}, '{product_id}', {qty})"
            )
        # Fun thing to do: randomise the following so we don't get paid or total
        total += cost
        possible_status = ["PAID", "PENDING"]
        status = random.choice(possible_status)
        cursor.execute(
            f"INSERT INTO invoices VALUES ({order_id}, '{order_id}', '{status}')"
        )
        if status == "PAID":
            paid += cost
    logger.info("Orders and invoices tables populated")
    logger.info(f"Total value in: {total}")
    logger.warning(f"Total value paid: {paid}")


if __name__ == "__main__":
    configure_logger()
    logger.setLevel(logging.INFO)
    clean()
    connection = sqlite3.connect(PLAYGROUND)
    cursor: Cursor = connection.cursor()
    add_products(cursor)
    connection.commit()
    generate_orders_and_invoices(cursor)
    connection.commit()
