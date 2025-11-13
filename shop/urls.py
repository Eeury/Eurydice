from django.urls import path

from . import views


app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("categories/", views.category_list, name="category_list"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/<slug:slug>/", views.cart_add, name="cart_add"),
    path("cart/remove/<slug:slug>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("signup/", views.signup, name="signup"),
]


