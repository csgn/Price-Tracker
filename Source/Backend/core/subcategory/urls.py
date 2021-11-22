from django.urls import path


from .views import (
    subcategories_subcategory_supplier_view, subcategories_subcategory_brands_view,
    subcategories_subcategory_categories_view, subcategories_subcategory_product_view,
    subcategories_view, subcategories_subcategory_view,
)

urlpatterns = [
    path('', subcategories_view),
    path('<int:subcategoryid>/', subcategories_subcategory_view),
    path('<int:subcategoryid>/category/',
         subcategories_subcategory_categories_view),
    path('<int:subcategoryid>/brand/', subcategories_subcategory_brands_view),
    path('<int:subcategoryid>/supplier/',
         subcategories_subcategory_supplier_view),
    path('<int:subcategoryid>/product/', subcategories_subcategory_product_view),
]
