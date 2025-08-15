from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("shop/", views.shop_view, name="shop"),
    path("add-to-cart/<int:pid>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart,name="cart"),
    path("remove-from-cart/<int:pid>/", views.remove_from_cart, name="remove_from_cart"),
] 