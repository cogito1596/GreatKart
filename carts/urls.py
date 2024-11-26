from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart, name="cart"),
    path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),
    path(
        "decrease_cart_item/<int:product_id>/",
        views.decrease_cart_item,
        name="decrease_cart_item",
    ),
    path(
        "remove-cart/<int:product_id>/<int:cart_item_id>/",
        views.remove_cart,
        name="remove-cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
]
