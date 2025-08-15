from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("shop/", views.shop_view, name="shop"),
    path("category/<int:cid>/", views.category_view, name="category"),
    path("product/<int:pid>/", views.product_detail, name="product_detail"),
    path("add-to-cart/<int:pid>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="cart"),
    path("remove-from-cart/<int:pid>/", views.remove_from_cart, name="remove-from-cart"),
    path("category/<int:cid>/", views.category_view, name="category"),
]