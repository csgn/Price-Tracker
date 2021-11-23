from util import makeQuery, convertToPSQL


def categories_view(request):
    if request.method == 'GET':
        return makeQuery(f"""
            select * from category
        """)


def categories_category_view(request, categoryid):
    if request.method == 'GET':
        return makeQuery(f"""
            select * from category where categoryid = {categoryid}
        """)

    elif request.method == 'PUT':
        import json
        props = convertToPSQL(json.loads(request.body))

        return makeQuery(f"""
            update category
                set {props}
            where categoryid = {categoryid}
        """, False)

    elif request.method == 'DELETE':
        return makeQuery(f"""
            delete
                from category
            where categoryid = {categoryid}
        """, False)


def categories_category_subcategories_view(request, categoryid):
    if request.method == 'GET':
        return makeQuery(f"""
            select sub.subcategoryid, sub.name, sub.url, sub.categoryid
                from category cat
                    join subcategory sub
                        on sub.categoryid = cat.categoryid
            where cat.categoryid = {categoryid}
        """)


def categories_category_brands_view(request, categoryid):
    if request.method == 'GET':
        return makeQuery(f"""
            select br.brandid, br.name, br.url
                from category cat
                    join categoryownedbybrand cobb
                        on cobb.categoryid = cat.categoryid
                    join brand br
                        on br.brandid = cobb.brandid
            where cat.categoryid = {categoryid}
        """)


def categories_category_supplier_view(request, categoryid):
    if request.method == 'GET':
        return makeQuery(f"""
            select supp.supplierid, supp.name, supp.rate, supp.url
                from category cat
                    join categoryownedbysupplier cobs
                        on cobs.categoryid = cat.categoryid
                    join supplier supp
                        on supp.supplierid = cobs.supplierid
            where cat.categoryid = {categoryid}
        """)


def categories_category_product_view(request, categoryid):
    if request.method == 'GET':
        return makeQuery(f"""
            select 
                prod.productid,
                prod.name,
                prod.images,
                prod.url,
                prod.rate,
                prod.brandid,
                prod.categoryid
                from category cat
                    join product prod
                        on prod.categoryid = cat.categoryid
            where cat.categoryid = {categoryid}
        """)
