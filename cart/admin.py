from django.contrib import admin
from .models import DirectPayment, MercadoPagoPayment, ItemsPayed

# Register your models here.

class DirectPaymentAdmin(admin.ModelAdmin):
    list_filter = ("date_order_created", "is_payed")
    list_display = ("order", "total_amount", "is_payed", "is_canceled")
    

class MercadoPagoPaymentAdmin(admin.ModelAdmin):
    list_filter = ("date_created", "status")
    list_display = ("payment_id", "total_amount", "status", "payment_method_id")

class ItemsPayedAdmin(admin.ModelAdmin):
    list_filter = ("title", )
    list_display = ("item_id", "title")

admin.site.register(DirectPayment, DirectPaymentAdmin)
admin.site.register(MercadoPagoPayment, MercadoPagoPaymentAdmin)
admin.site.register(ItemsPayed, ItemsPayedAdmin)