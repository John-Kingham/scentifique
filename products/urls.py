from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/", views.ProductDetail.as_view(), name="product_detail"),
    path("add/", views.add_product, name="add_product"),
    path(
        "delete/<int:product_id>/", views.delete_product, name="delete_product"
    ),
    path("edit/<int:product_id>/", views.edit_product, name="edit_product"),
    path("", views.ProductList.as_view(), name="products"),
]
