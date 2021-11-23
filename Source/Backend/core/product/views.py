from django.http.response import HttpResponse

from util import makeQuery, convertToPSQL


def products_view(request):
    if request.method == 'GET':
        return makeQuery(f"""
            select * from product
        """)


def products_product_view(request, productid):
    if request.method == 'GET':
        return makeQuery(f"""
            select * from product where productid = {productid}
        """)

    elif request.method == 'POST':
        return HttpResponse("posted")

    elif request.method == 'PUT':
        import json
        props = convertToPSQL(json.loads(request.body))

        return makeQuery(f"""
            update product
                set {props}
            where productid = {productid}
        """, False)

    elif request.method == 'DELETE':
        return makeQuery(f"""
            delete
                from product
            where productid = {productid}
        """, False)


def products_product_price_view(request, productid):
    if request.method == 'GET':
        return makeQuery(f"""
            select 
                p.priceid,
                p.amount,
                p.startdate,
                p.supplierid
            from price p
                join productownedbysupplier pobs
                    on pobs.productid = p.productid 
                    and pobs.supplierid = p.supplierid
            where p.productid = {productid}
            order by p.amount
        """)


def products_product_subcategories_view(request, productid):
    if request.method == 'GET':
        return makeQuery(f"""
            select sub.subcategoryid, sub.name, sub.url, sub.categoryid
                from product prod
                    join productownedbysubcategory pobs
                        on pobs.productid = prod.productid
                    join subcategory sub
                        on sub.subcategoryid = pobs.subcategoryid
            where prod.productid={productid}
        """)


def products_product_categories_view(request, productid):
    if request.method == 'GET':
        return makeQuery(f"""
            select cat.categoryid, cat.name, cat.url
                from product prod
                    join category cat
                        on cat.categoryid = prod.categoryid
            where prod.productid = {productid}
        """)


def products_product_brand_view(request, productid):
    if request.method == 'GET':
        return makeQuery(f"""
            select br.brandid, br.name, br.url
                from product prod
                    join brand br
                        on br.brandid = prod.brandid
            where prod.productid = {productid}
        """)


def products_product_suppliers_view(request, productid):
    if request.method == 'GET':
        return makeQuery(f"""
            select supp.supplierid, supp.name, supp.rate, supp.url
                from supplier supp
                    join productownedbysupplier pobs
                        on pobs.supplierid = supp.supplierid
            where pobs.productid = {productid}
        """)
