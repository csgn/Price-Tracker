from django.http import JsonResponse

from util import makeQuery


def suppliers_view(request):
    if request.method == 'GET':
        return makeQuery(f"""
            select * from supplier
        """)


def suppliers_supplier_view(request, supplierid=None):
    if request.method == 'GET':
        return makeQuery(f"""
            select * from supplier where supplierid = {supplierid}
        """)


def suppliers_supplier_subcategories_view(request, supplierid):
    if request.method == 'GET':
        return makeQuery(f"""
            select sub.subcategoryid, sub.name, sub.url, sub.categoryid
                from supplier supp
                    join subcategoryownedbysupplier sobs
                        on sobs.supplierid = supp.supplierid
                    join subcategory sub
                        on sub.subcategoryid = sobs.subcategoryid
            where supp.supplierid = {supplierid}
        """)


def suppliers_supplier_categories_view(request, supplierid):
    if request.method == 'GET':
        return makeQuery(f"""
            select cat.categoryid, cat.name, cat.url
                from supplier supp
                    join categoryownedbysupplier cobs
                        on cobs.supplierid = supp.supplierid
                    join category cat
                        on cat.categoryid = cobs.categoryid
            where supp.supplierid = {supplierid}
        """)


def suppliers_supplier_brand_view(request, supplierid):
    if request.method == 'GET':
        return makeQuery(f"""
            select br.brandid, br.name, br.url
                from brand br
                    join brandownedbysupplier bobs
                        on bobs.brandid = br.brandid
                    join supplier supp
                        on supp.supplierid = bobs.supplierid
            where supp.supplierid = {supplierid}
        """)


def suppliers_supplier_product_view(request, supplierid):
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
                from supplier supp
                    join productownedbysupplier pobs
                        on pobs.supplierid = supp.supplierid
                    join product prod
                        on prod.productid = pobs.productid
            where supp.supplierid = {supplierid}
        """)
