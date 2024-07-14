from django.urls import path
from . import views

urlpatterns = [
    path("change-and-devolutions", views.ChangeDevolutionView.as_view(), name="change-devolutions"),
    path("privacy", views.PrivacityView.as_view(), name="privacy"),
    path("shipments", views.ShipmentsView.as_view(), name="shipments"),
    path("terms-and-conditions", views.TermsConditionsView.as_view(), name="terms-and-conditions"),
]