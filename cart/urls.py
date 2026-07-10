from django.urls import path
from . import views

urlpatterns = [
    path("", views.CartView.as_view(), name="view_cart"),
    path(
        "add/<int:product_id>/", views.AddToCart.as_view(), name="add_to_cart"
    ),
    path(
        "remove/<cart_item_key>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("update/<cart_item_key>/", views.update_cart, name="update_cart"),
]
