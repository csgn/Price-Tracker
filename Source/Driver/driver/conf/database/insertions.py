import conf.database as db
from conf.scripts.altcursor import AlterCursor
import conf.scripts.time as time


def __INSERT_RELATION__(*args, **kwargs):
    id1_name, id2_name = args[0].keys()
    id1, id2 = args[0].values()
    table = list(kwargs.values())[0]

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT {id1_name}, {id2_name} from {table}
                WHERE ({id1_name}={id1} and {id2_name}={id2});
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
            INSERT INTO {table} ({id1_name}, {id2_name})
                VALUES (
                    {id1},
                    {id2}
                )
        """)


def __INSERT_ROW__(*, attrs, table, isdistinct=None):
    keys, values = list(attrs.keys()), list(attrs.values())

    res = None
    if isdistinct:
        with AlterCursor() as altcur:
            altcur.cursor.execute(f"""
                SELECT {isdistinct['row']} from {table}
                    WHERE url='{attrs['url']}'
            """)
            res = altcur.fetch()

    if res:
        return res

    q = ""
    for i in values:
        if type(i) is str and i != 'null' and "startdate" not in keys:
            q += f"'{i}'"
        else:
            q += str(i)
        q += ','

    q = q[:-1]

    db.cursor.execute(f"""
        INSERT INTO {table} ({",".join(keys)})
            VALUES (
                {q}
            )
            RETURNING {table + 'id'};
    """)

    return db.cursor.fetchone()[0]


def insert(other):
    name = other["product name"]
    url = other["url"]
    rate = "null" if other["rate"] is None else other["rate"]
    images = '{' + ",".join(f'"{image}"' for image in other["images"]) + '}'

    brandid = __INSERT_ROW__(attrs=other["brand"], table="brand", isdistinct={
        "row": "brandid"})

    categoryid = __INSERT_ROW__(attrs=other["category"], table="category", isdistinct={
        "row": "categoryid"})

    __INSERT_RELATION__(
        {"brandid": brandid, "categoryid": categoryid}, table="categoryownedbybrand")

    productid = __INSERT_ROW__(attrs={
        "name": name, "images": images, "url": url,
        "rate": rate, "brandid": brandid,
        "categoryid": categoryid}, table="product")

    supplierids = []
    for supplier in other["supplier"]:
        supplier_price = supplier['price']
        del supplier['price']

        supplier["rate"] = "null" if supplier["rate"] is None else supplier["rate"]
        supplierid = __INSERT_ROW__(attrs=supplier, table="supplier", isdistinct={
            "row": "supplierid"})

        priceid = __INSERT_ROW__(
            attrs={"amount": supplier_price, "startdate": f"to_timestamp('{time.now()}', 'yyyy-mm-dd hh24:mi:ss')", "supplierid": supplierid}, table="price")

        __INSERT_RELATION__(
            {"supplierid": supplierid, "brandid": brandid}, table="brandownedbysupplier")

        __INSERT_RELATION__(
            {"supplierid": supplierid, "categoryid": categoryid}, table="categoryownedbysupplier")

        __INSERT_RELATION__(
            {"supplierid": supplierid, "productid": productid}, table="productownedbysupplier")
        supplierids.append(supplierid)

    for subcategory in other["subcategory"]:
        subcategoryid = __INSERT_ROW__(attrs={**subcategory, "categoryid": categoryid}, table="subcategory", isdistinct={
            "row": "subcategoryid"})

        __INSERT_RELATION__(
            {"brandid": brandid, "subcategoryid": subcategoryid}, table="subcategoryownedbybrand")

        __INSERT_RELATION__(
            {"subcategoryid": subcategoryid, "productid": productid}, table="productownedbysubcategory")
        for supplierid in supplierids:
            __INSERT_RELATION__(
                {"supplierid": supplierid, "subcategoryid": subcategoryid}, table="subcategoryownedbysupplier")
    db.connection.commit()
