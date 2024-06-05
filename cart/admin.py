from django.contrib import admin
from .models import DirectPayments, MercadoPagoPayment, ItemsPayed

# Register your models here.

class DirectPaymentAdmin(admin.ModelAdmin):
    list_filter = ("date_order_created", "status", )
    list_display = ("order", "total_amount", "status", "date_order_created")
    search_fields = ("order", )

class MercadoPagoPaymentAdmin(admin.ModelAdmin):
    list_filter = ("date_created", "status")
    list_display = ("payment_id", "total_amount", "status", "date_created")
    search_fields = ("merchand_order", "payment_id")

class ItemsPayedAdmin(admin.ModelAdmin):
    list_filter = ("title", )
    list_display = ("title", "direct_payment", "mercadopago_payment")
    search_fields = ("direct_payment__order", "mercadopago_payment__payment_id") 

admin.site.register(DirectPayments, DirectPaymentAdmin)
admin.site.register(MercadoPagoPayment, MercadoPagoPaymentAdmin)
admin.site.register(ItemsPayed, ItemsPayedAdmin)