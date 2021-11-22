from django.http import JsonResponse

from util import makeQuery


def subcategories_view(request):
    if request.method == 'GET':
        return makeQuery(f"""
            select * from subcategory
        """)


def subcategories_subcategory_view(request, subcategoryid=None):
    if request.method == 'GET':
        return makeQuery(f"""
            select * from subcategory where subcategoryid = {subcategoryid}
        """)


def subcategories_subcategory_categories_view(request, subcategoryid):
    if request.method == 'GET':
        return makeQuery(f"""
            select cat.categoryid, cat.name, cat.url
                from category cat
                    join subcategory sub
                        on sub.categoryid = cat.categoryid
            where sub.subcategoryid = {subcategoryid}
        """)


def subcategories_subcategory_brands_view(request, subcategoryid):
    if request.method == 'GET':
        return makeQuery(f"""
            select br.brandid, br.name, br.url
                from subcategory sub
                    join subcategoryownedbybrand sobb
                        on sobb.subcategoryid = sub.subcategoryid
                    join brand br
                        on br.brandid = sobb.brandid
            where sub.subcategoryid = {subcategoryid}
        """)


def subcategories_subcategory_supplier_view(request, subcategoryid):
    if request.method == 'GET':
        return makeQuery(f"""
            select supp.supplierid, supp.name, supp.rate, supp.url
                from subcategory sub
                    join subcategoryownedbysupplier sobs
                        on sobs.subcategoryid = sub.subcategoryid
                    join supplier supp
                        on supp.supplierid = sobs.supplierid
            where sub.subcategoryid = {subcategoryid}
        """)


def subcategories_subcategory_product_view(request, subcategoryid):
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
                from subcategory sub
                    join productownedbysubcategory pobs
                        on pobs.subcategoryid = sub.subcategoryid
                    join product prod
                        on prod.productid = pobs.productid
            where sub.subcategoryid = {subcategoryid}
        """)
