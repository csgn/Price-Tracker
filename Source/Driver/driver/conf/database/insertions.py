import conf.database as db
from conf.scripts.altcursor import AlterCursor
import conf.scripts.util as util


def __INSERT_RELATION__(*args, **kwargs):
    table = list(kwargs.values())[0]
    columns = args[0].keys()
    values = list(map(lambda x: str(x), args[0].values()))
    where = " and ".join(
        list(map(lambda p: f"{p[0]} = {p[1]}", list(zip(columns, values)))))

    columns = ",".join(columns)
    values = ",".join(values)

    with AlterCursor() as altcur:
        altcur.cursor.execute(f"""
            SELECT {columns} from {table}
                WHERE ({where});
        """)
        res = altcur.fetch()

    if not res:
        db.cursor.execute(f"""
            INSERT INTO {table} ({columns})
                VALUES (
                    {values}
                )
        """)


def __INSERT_ROW__(*, attrs, table, ifexists=None):
    keys, values = list(attrs.keys()), list(attrs.values())

    res = None
    if ifexists and table != "price":
        with AlterCursor() as altcur:
            altcur.cursor.execute(f"""
                SELECT {ifexists['row']} from {table}
                    WHERE url='{attrs['url']}'
            """)
            res = altcur.fetch()

    if res:
        return res

    q = ""
    for i in values:
        if type(i) is str and i != 'null':
            q += f"'{i}'"
        else:
            q += str(i)
        q += ','

    db.cursor.execute(f"""
        INSERT INTO {table} ({",".join(keys)})
            VALUES (
                {q[:-1]}
            )
            RETURNING {table + 'id'};
    """)

    return db.cursor.fetchone()[0]


def insert(other):
    name = other["product name"]
    url = other["url"]
    rate = "null" if other["rate"] is None else other["rate"]
    images = '{' + ",".join(f'"{image}"' for image in other["images"]) + '}'

    brandid = __INSERT_ROW__(attrs=other["brand"], table="brand", ifexists={
        "row": "brandid"})

    categoryid = __INSERT_ROW__(attrs=other["category"], table="category", ifexists={
        "row": "categoryid"})

    __INSERT_RELATION__(
        {"brandid": brandid, "categoryid": categoryid}, table="categoryownedbybrand")

    productid = __INSERT_ROW__(attrs={
        "name": name, "images": images, "url": url,
        "rate": rate, "brandid": brandid,
        "categoryid": categoryid}, table="product", ifexists={"row": "productid"})

    supplierids = []
    for supplier in other["supplier"]:
        supplier_price = supplier['price']
        del supplier['price']

        supplier["rate"] = "null" if supplier["rate"] is None else supplier["rate"]
        supplierid = __INSERT_ROW__(attrs=supplier, table="supplier", ifexists={
            "row": "supplierid"})

        priceid = __INSERT_ROW__(
            attrs={"amount": supplier_price, "supplierid": supplierid, "productid": productid}, table="price")

        __INSERT_RELATION__(
            {"supplierid": supplierid, "brandid": brandid}, table="brandownedbysupplier")

        __INSERT_RELATION__(
            {"supplierid": supplierid, "categoryid": categoryid}, table="categoryownedbysupplier")

        __INSERT_RELATION__(
            {"supplierid": supplierid, "productid": productid}, table="productownedbysupplier")
        supplierids.append(supplierid)

    for subcategory in other["subcategory"]:
        subcategoryid = __INSERT_ROW__(attrs={**subcategory, "categoryid": categoryid}, table="subcategory", ifexists={
            "row": "subcategoryid"})

        __INSERT_RELATION__(
            {"brandid": brandid, "subcategoryid": subcategoryid}, table="subcategoryownedbybrand")

        __INSERT_RELATION__(
            {"subcategoryid": subcategoryid, "productid": productid}, table="productownedbysubcategory")
        for supplierid in supplierids:
            __INSERT_RELATION__(
                {"supplierid": supplierid, "subcategoryid": subcategoryid}, table="subcategoryownedbysupplier")
    db.connection.commit()
