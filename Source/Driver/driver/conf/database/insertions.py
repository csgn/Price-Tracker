import conf.global_settings as settings
import conf.database as db
from conf.scripts.altcursor import AlterCursor
import conf.scripts.time as time


def __getid(fun) -> int:
    def wrapper(*args):
        res = fun(args if len(args) > 1 else args[0])
        return db.cursor.fetchone()[0] if not res else res

    return wrapper


@__getid
def __INSERT__PRODUCT(*args) -> None:
    product = args[0]
    name, images, url, rate, brandid, categoryid = product.values()

    db.cursor.execute(f"""
    INSERT INTO product (name, images, url, rate, brandid, categoryid)
        VALUES (
            '{name}',
            '{images}',
            '{url}',
            {'null' if rate is None else rate},
            {brandid},
            {categoryid}
        )
        RETURNING productid;
    """)


@__getid
def __INSERT__BRAND(*args) -> int:
    brand = args[0]
    name, url = brand.values()

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT brandid from brand
            WHERE url='{url}'
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
        INSERT INTO brand (name, url)
            VALUES (
                '{name}',
                '{url}'
            )
            RETURNING brandid;
        """)
    else:
        return res


@__getid
def __INSERT__PRICE(*args) -> None:
    price = args[0]
    supplierid, amount = price.values()
    current_date = time.now()

    db.cursor.execute(f"""
    INSERT INTO price (amount, startdate, supplierid)
        VALUES (
            '{amount}',
            to_timestamp('{current_date}', 'yyyy-mm-dd hh24:mi:ss'),
            {supplierid}
        )
        RETURNING priceid;
    """)


@__getid
def __INSERT__SUPPLIER(*args) -> int:
    supplier = args[0]
    name, rate, url, _ = supplier.values()

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT supplierid from supplier
                WHERE url='{url}'
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
        INSERT INTO supplier (name, rate, url)
            VALUES (
                '{name}',
                {'null' if rate is None else rate},
                '{url}'
            )
            RETURNING supplierid;
        """)
    else:
        return res


@__getid
def __INSERT__CATEGORY(*args) -> None:
    category = args[0]
    name, url = category.values()

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT categoryid from category
                WHERE url='{url}';
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
            INSERT INTO category (name, url)
                VALUES (
                    '{name}',
                    '{url}'
            )
            RETURNING categoryid;
        """)
    else:
        return res


@__getid
def __INSERT__SUBCATEGORY(*args) -> None:
    subcategory = args[0]
    name, url, categoryid = subcategory.values()

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT subcategoryid from subcategory
                WHERE url='{url}';
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
            INSERT INTO subcategory (name, url, categoryid)
                VALUES (
                    '{name}',
                    '{url}',
                    {categoryid}
                )
                RETURNING subcategoryid;
        """)
    else:
        return res


def __INSERT__CATEGORYOWNEDBYBRAND(*args) -> None:
    brandid, categoryid = args[0].values()

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT brandid, categoryid from categoryownedbybrand
                WHERE (brandid={brandid} and categoryid={categoryid});
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
            INSERT INTO categoryownedbybrand (brandid, categoryid)
                VALUES (
                    {brandid},
                    {categoryid}
                )
        """)


def __INSERT__CATEGORYOWNEDBYSUPPLIER(*args):
    supplierid, categoryid = args[0].values()

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT supplierid, categoryid from categoryownedbysupplier
                WHERE (supplierid={supplierid} and categoryid={categoryid});
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
            INSERT INTO categoryownedbysupplier (supplierid, categoryid)
                VALUES (
                    {supplierid},
                    {categoryid}
                )
        """)


def __INSERT__BRANDOWNEDBYSUPPLIER(*args):
    supplierid, brandid = args[0].values()

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT supplierid, brandid from brandownedbysupplier
                WHERE (supplierid={supplierid} and brandid={brandid});
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
            INSERT INTO brandownedbysupplier (supplierid, brandid)
                VALUES (
                    {supplierid},
                    {brandid}
                )
        """)


def __INSERT__PRODUCTOWNEDBYSUPPLIER(*args):
    supplierid, productid = args[0].values()

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT supplierid, productid from productownedbysupplier
                WHERE (supplierid={supplierid} and productid={productid});
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
            INSERT INTO productownedbysupplier (supplierid, productid)
                VALUES (
                    {supplierid},
                    {productid}
                )
        """)


def __INSERT__PRODUCTOWNEDBYSUBCATEGORY(*args):
    subcategoryid, productid = args[0].values()

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT subcategoryid, productid from productownedbysubcategory
                WHERE (subcategoryid={subcategoryid} and productid={productid});
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
            INSERT INTO productownedbysubcategory (subcategoryid, productid)
                VALUES (
                    {subcategoryid},
                    {productid}
                )
        """)


def __INSERT__SUBCATEGORYOWNEDBYSUPPLIER(*args):
    supplierid, subcategoryid = args[0].values()

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT supplierid, subcategoryid from subcategoryownedbysupplier
                WHERE (supplierid={supplierid} and subcategoryid={subcategoryid});
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
            INSERT INTO subcategoryownedbysupplier (supplierid, subcategoryid)
                VALUES (
                    {supplierid},
                    {subcategoryid}
                )
        """)


def __INSERT__SUBCATEGORYOWNEDBYBRAND(*args):
    brandid, subcategoryid = args[0].values()

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT brandid, subcategoryid from subcategoryownedbybrand 
                WHERE (brandid={brandid} and subcategoryid={subcategoryid});
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
            INSERT INTO subcategoryownedbybrand (brandid, subcategoryid)
                VALUES (
                    {brandid},
                    {subcategoryid}
                )
        """)
    pass


def insert(other):
    name = other["product name"]
    url = other["url"]
    rate = other["rate"]

    images = '{' + ",".join(f'"{image}"' for image in other["images"]) + '}'

    brandid = __INSERT__BRAND(other["brand"])
    categoryid = __INSERT__CATEGORY(other["category"])

    __INSERT__CATEGORYOWNEDBYBRAND(
        {"brandid": brandid, "categoryid": categoryid})

    productid = __INSERT__PRODUCT({
        "name": name,
        "images": images,
        "url": url,
        "rate": rate,
        "brandid": brandid,
        "categoryid": categoryid
    })

    supplierids = []
    for supplier in other["supplier"]:
        supplierid = __INSERT__SUPPLIER(supplier)
        priceid = __INSERT__PRICE(
            {"supplierid": supplierid, "amount": supplier["price"]})

        __INSERT__BRANDOWNEDBYSUPPLIER(
            {"supplierid": supplierid, "brandid": brandid})
        __INSERT__CATEGORYOWNEDBYSUPPLIER(
            {"supplierid": supplierid, "categoryid": categoryid})
        __INSERT__PRODUCTOWNEDBYSUPPLIER(
            {"supplierid": supplierid, "productid": productid})

        supplierids.append(supplierid)

    for subcategory in other["subcategory"]:
        subcategoryid = __INSERT__SUBCATEGORY(
            {**subcategory, "categoryid": categoryid})
        __INSERT__SUBCATEGORYOWNEDBYBRAND(
            {"brandid": brandid, "subcategoryid": subcategoryid})
        __INSERT__PRODUCTOWNEDBYSUBCATEGORY(
            {"subcategoryid": subcategoryid, "productid": productid})

        for supplierid in supplierids:
            __INSERT__SUBCATEGORYOWNEDBYSUPPLIER(
                {"supplierid": supplierid, "subcategoryid": subcategoryid})

    db.connection.commit()
