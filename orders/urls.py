from django.urls import path
from . import views


urlpatterns = [
    path("checkout/", views.place_order, name="order"),
]
