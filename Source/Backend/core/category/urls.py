from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    categories_category_supplier_view, categories_category_brands_view,
    categories_category_subcategories_view, categories_category_product_view,
    categories_view, categories_category_view,
)

urlpatterns = [
    path('', categories_view),
    path('<int:categoryid>/', csrf_exempt(categories_category_view)),
    path('<int:categoryid>/subcategory/',
         categories_category_subcategories_view),
    path('<int:categoryid>/brand/', categories_category_brands_view),
    path('<int:categoryid>/supplier/', categories_category_supplier_view),
    path('<int:categoryid>/product/', categories_category_product_view),
]
