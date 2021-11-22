from django.urls import path

from .views import (
    brands_brand_supplier_view, brands_brand_categories_view,
    brands_brand_subcategories_view, brands_brand_product_view,
    brands_view, brands_brand_view,
)

urlpatterns = [
    path('', brands_view),
    path('<int:brandid>/', brands_brand_view),
    path('<int:brandid>/subcategory/',
         brands_brand_subcategories_view),
    path('<int:brandid>/category/', brands_brand_categories_view),
    path('<int:brandid>/supplier/', brands_brand_supplier_view),
    path('<int:brandid>/product/', brands_brand_product_view),
]
