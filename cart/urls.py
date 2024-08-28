from django.urls import path
from . import views

app_name = "cart" 

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("remove/", views.remove_product_from_cart, name="remove_product_from_cart"),
    path("add/", views.add_product_to_cart, name="add_product_to_cart"),
]
