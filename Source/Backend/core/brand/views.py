from django.http import JsonResponse

from util import makeQuery


def brands_view(request):
    if request.method == 'GET':
        return makeQuery(f"""
            select * from brand
        """)


def brands_brand_view(request, brandid=None):
    if request.method == 'GET':
        return makeQuery(f"""
            select * from brand where brandid = {brandid}
        """)


def brands_brand_subcategories_view(request, brandid):
    if request.method == 'GET':
        return makeQuery(f"""
            select sub.subcategoryid, sub.name, sub.url, sub.categoryid
                from brand br
                    join subcategoryownedbybrand sobs
                        on sobs.brandid = br.brandid
                    join subcategory sub
                        on sub.subcategoryid = sobs.subcategoryid
            where br.brandid = {brandid}
        """)


def brands_brand_categories_view(request, brandid):
    if request.method == 'GET':
        return makeQuery(f"""
            select cat.categoryid, cat.name, cat.url
                from brand br
                    join categoryownedbybrand cobs
                        on cobs.brandid = br.brandid
                    join category cat
                        on cat.categoryid = cobs.categoryid
            where br.brandid = {brandid}
        """)


def brands_brand_supplier_view(request, brandid):
    if request.method == 'GET':
        return makeQuery(f"""
            select supp.supplierid, supp.name, supp.rate, supp.url
                from brand br
                    join brandownedbysupplier bobs
                        on bobs.brandid = br.brandid
                    join supplier supp
                        on supp.supplierid = bobs.supplierid
            where br.brandid = {brandid}
        """)


def brands_brand_product_view(request, brandid):
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
                from brand br
                    join product prod
                        on prod.brandid = br.brandid
            where br.brandid = {brandid}
        """)
