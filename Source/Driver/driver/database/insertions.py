from typing import Dict, Any
from datetime import date

import database as db


def __INSERT__PRODUCT():
    pass


def __INSERT__BRAND():
    pass


def __INSERT__PRICE():
    pass


def __INSERT__RATE(rate: str) -> int:
    from datetime import datetime
    current_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

    db.cursor.execute(f"""
    INSERT INTO rate (score, date)
        VALUES (
            {float(rate) if rate else '0.0'},
            to_timestamp('{current_date}', 'yyyy-mm-dd hh24:mi:ss')
        )
        RETURNING rateid;
    """)

    return db.cursor.fetchone()[0]


def __INSERT_IMAGES():
    pass


def __INSERT__SUPPLIER(supplier) -> int:
    name, rate, url, _ = supplier.values()

    db.cursor.execute(f"""
    INSERT INTO supplier (name, rateid, url)
        VALUES (
            '{name}',
            {__INSERT__RATE(rate)},
            '{url}'
        )
        RETURNING supplierid;
    """)

    return db.cursor.fetchone()[0]


def __INSERT__CATEGORY():
    pass


def __INSERT__SUBCATEGORY():
    pass


def insert_to_db(other):
    product_rateid = __INSERT__RATE(other["rate"])

    for supplier in other["supplier"]:
        supplierid = __INSERT__SUPPLIER(supplier)

    db.connection.commit()
