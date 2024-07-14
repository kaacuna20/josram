from django.urls import path
from . import views

urlpatterns = [

    path("", views.CartView.as_view(), name="your-cart"),
    path("checkout", views.CheckOutView.as_view(), name="checkout-buy"),
    path("payment-methods", views.ReferenceView.as_view(), name="mercadopago-payment"),
    #path("success", views.success),
    #path("failure", views.failure),
    #path("pending", views.supend),
    path("success", views.SuccessView.as_view(), name="success-notification"),
    path("failure", views.FailureView.as_view(), name="failure-notification"),
    path("pending", views.SuspendView.as_view(), name="suspend-notification"),
    
    path("notification", views.NotificationView.as_view(), name='notification_handler'),
    path("direct-payment/<int:id_order>", views.DirectPayment.as_view(), name='direct-payment'),

]
