from django.urls import path

from .views import (
    products_product_brand_view, products_product_categories_view,
    products_product_subcategories_view, products_product_suppliers_view,
    products_view, products_product_view, products_product_price_view
)

urlpatterns = [
    path('', products_view),
    path('<int:productid>/', products_product_view),
    path('<int:productid>/price/', products_product_price_view),
    path('<int:productid>/subcategory/', products_product_subcategories_view),
    path('<int:productid>/category/', products_product_categories_view),
    path('<int:productid>/brand/', products_product_brand_view),
    path('<int:productid>/supplier/', products_product_suppliers_view),
]
