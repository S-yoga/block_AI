

from django.urls import path
from . import views

urlpatterns =[
    #path("", views.register_view, name="register"),
    path("register_url/", views.register_view, name="register"),
    path("login_url/",views.login_view,name="login"),
    path("shop_url/", views.shop_view, name="shop"),
    # path("shop/", views.shop_view, name="shop"),                      # main shop page
    # path("product/<int:pid>/", views.product_detail, name="product_detail"),
    path("add-to-cart/<int:pid>/", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:pid>/", views.remove_from_cart, name="remove_from_cart"),
    path("view_cart/", views.view_cart,name="view_cart"),
    path("logout/",views.logout_view,name="logout"),
]