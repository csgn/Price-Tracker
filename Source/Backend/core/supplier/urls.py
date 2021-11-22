from django.urls import path

from .views import (
    suppliers_supplier_brand_view, suppliers_supplier_categories_view,
    suppliers_supplier_subcategories_view, suppliers_supplier_product_view,
    suppliers_view, suppliers_supplier_view,
)

urlpatterns = [
    path('', suppliers_view),
    path('<int:supplierid>/', suppliers_supplier_view),
    path('<int:supplierid>/subcategory/',
         suppliers_supplier_subcategories_view),
    path('<int:supplierid>/category/', suppliers_supplier_categories_view),
    path('<int:supplierid>/brand/', suppliers_supplier_brand_view),
    path('<int:supplierid>/product/', suppliers_supplier_product_view),
]
