from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartPageView.as_view(), name="start-page"),
    path("products/all", views.AllProducts.as_view(), name="all-products"),
    path("collection/<gender>", views.ClothesByGender.as_view(), name="gender-clothes"),
    path("collections/<slug:slug_type>", views.ClothesByType.as_view(), name="type-clothes"),
    #path("clothe/<slug:slug>", views.clothe_details, name="clothes-details"),
    path("clothe/<slug:slug>", views.ClotheDetailView.as_view(), name="clothes-details"),
    path('search/', views.SearhView.as_view(), name='search'),
]
