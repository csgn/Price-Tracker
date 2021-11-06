from typing import Dict, Any
from datetime import datetime

import database as db


def gettimestamp():
    return (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")


def getid(fun) -> int:
    def wrapper(*args, **kwargs):
        fun(args if len(args) > 1 else args[0])
        return db.cursor.fetchone()[0]

    return wrapper


@getid
def __INSERT__PRODUCT(*args) -> None:
    rateid, brandid, priceid, categoryid, name, url, images = args[0]
    images = '{' + ",".join(f'"{image}"' for image in images) + '}'

    name = name.replace("'", "")

    db.cursor.execute(f"""
    INSERT INTO product (name, images, url, rateid, priceid, brandid, categoryid)
        VALUES (
            '{name}',
            '{images}',
            '{url}',
            {rateid},
            {priceid},
            {brandid},
            {categoryid}
        )
        RETURNING productid;
    """)


@getid
def __INSERT__BRAND(brand) -> None:
    name, url = brand.values()

    name = name.replace("'", "")
    db.cursor.execute(f"""
    INSERT INTO brand (name, url)
        VALUES (
            '{name}',
            '{url}'
        )
        RETURNING brandid;
    """)


@getid
def __INSERT__PRICE(price: str) -> None:
    amount = float(price.split(',')[0])
    current_date = gettimestamp()

    db.cursor.execute(f"""
    INSERT INTO price (amount, startdate)
        VALUES (
            '{amount}',
            to_timestamp('{current_date}', 'yyyy-mm-dd hh24:mi:ss')
        )
        RETURNING priceid;
    """)


@getid
def __INSERT__RATE(rate: str) -> None:
    current_date = gettimestamp()

    db.cursor.execute(f"""
    INSERT INTO rate (score, date)
        VALUES (
            {float(rate) if rate else 0},
            to_timestamp('{current_date}', 'yyyy-mm-dd hh24:mi:ss')
        )
        RETURNING rateid;
    """)


@getid
def __INSERT__SUPPLIER(supplier) -> None:
    name, rate, url, _ = supplier.values()
    name = name.replace("'", "")

    db.cursor.execute(f"""
    INSERT INTO supplier (name, rateid, url)
        VALUES (
            '{name}',
            {__INSERT__RATE(rate)},
            '{url}'
        )
        RETURNING supplierid;
    """)


@getid
def __INSERT__CATEGORY(*args) -> None:
    category, subcategories_id = args[0]
    name, url = category.values()
    name = name.replace("'", "")

    for subcategoryid in subcategories_id:
        db.cursor.execute(f"""
        INSERT INTO category (name, url, subcategoryid)
            VALUES (
                '{name}',
                '{url}',
                {subcategoryid}
            )
            RETURNING categoryid;
        """)


@getid
def __INSERT__SUBCATEGORY(subcategory) -> None:
    name, url = subcategory.values()
    name = name.replace("'", "")

    db.cursor.execute(f"""
    INSERT INTO subcategory (name, url)
        VALUES (
            '{name}',
            '{url}'
        )
        RETURNING subcategoryid;
    """)


def insert_to_db(other):
    product_rateid = __INSERT__RATE(other["rate"])
    product_brandid = __INSERT__BRAND(other["brand"])

    subcategories_id = []
    for subcategory in other["subcategory"]:
        subcategoryid = __INSERT__SUBCATEGORY(subcategory)
        subcategories_id.append(subcategoryid)

    product_categoryid = __INSERT__CATEGORY(
        other["category"], subcategories_id)

    product_priceid = __INSERT__PRICE(other["price"])

    suppliers_id = []
    for supplier in other["supplier"]:
        supplierid = __INSERT__SUPPLIER(supplier)
        suppliers_id.append(supplierid)

    productid = __INSERT__PRODUCT(
        product_rateid, product_brandid,
        product_priceid, product_categoryid,
        other["product name"], other["url"],
        other["images"]
    )

    db.connection.commit()
