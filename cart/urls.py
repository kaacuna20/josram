from django.urls import path
from . import views

urlpatterns = [

    path("", views.CartView.as_view(), name="your-cart"),
    path("checkout", views.CheckOutView.as_view(), name="cheackout-buy"),
    path("payment-methods", views.ReferenceView.as_view(), name="form-payment"),
    path("success", views.success),
    path("failure", views.failure),
    path("pending", views.supend),
    path("notification", views.notificate, name='notification_handler'),

]