from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartPageView.as_view(), name="start-page"),
    path("collection", views.AllProducts.as_view(), name="all-products"),
    path("<gender>/clothes", views.show_clothes_by_gender, name="gender-clothes"),
    path("clothe/<slug:slug>", views.clothe_details, name="clothes-details"),
    #path("sales-cart", views.cart, name="your-cart"),
    path("sales-cart", views.CartView.as_view(), name="your-cart"),
    path("checkout", views.CheckOutView.as_view(), name="cheackout-buy")
]
