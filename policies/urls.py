from django.urls import path
from . import views

urlpatterns = [
    path("change-and-devolutions", views.change_devolutions, name="change-devolutions"),
    path("privacy", views.privacity, name="privacy"),
    path("shipments", views.shipments, name="shipments"),
    path("terms-and-conditions", views.terms_and_conditions, name="terms-and-conditions"),
]