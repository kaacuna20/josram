from django.db import models
from datetime import datetime, timedelta

# Create your models here.

current_day = datetime.now().isoformat()

class DirectPayment(models.Model):
    order = models.IntegerField()
    payer_fullname = models.CharField(max_length=100)
    payer_phone = models.CharField(max_length=10)
    payer_address = models.CharField(max_length=100)
    payer_email = models.EmailField()
    shipments = models.IntegerField()
    paid_amount = models.IntegerField()
    total_amount = models.IntegerField()
    date_order_created = models.DateField(auto_now=True)
    is_payed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
          current_day = datetime.now().isoformat()
          if current_day > self.date_order_created.isoformat() + timedelta(minutes=3) and self.is_payed == False:
               self.is_canceled = True
               super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order}"
    
class MercadoPagoPayment(models.Model):
    merchand_order = models.IntegerField()
    payment_id = models.IntegerField()
    paid_amount = models.IntegerField()
    shipping_cost = models.IntegerField()
    total_amount = models.IntegerField()
    net_received_amount = models.IntegerField()
    status = models.CharField(max_length=100)
    date_created = models.DateField(auto_now=False)
    order_status = models.CharField(max_length=100)
    payment_method_id = models.CharField(max_length=100)
    payment_type_id = models.CharField(max_length=100)
    payer_name = models.CharField(max_length=100)
    payer_lastname = models.CharField(max_length=100)
    payer_phone = models.CharField(max_length=10)
    payer_address = models.CharField(max_length=100)
    iva = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.merchand_order}"
    

class ItemsPayed(models.Model):
    item_id = models.CharField(max_length=100, default="None")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    direct_payment = models.ForeignKey(DirectPayment, related_name="direct_payment", on_delete=models.CASCADE, null=True)
    mercadopago_payment = models.ForeignKey(MercadoPagoPayment, related_name="mercadopago_payment", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}: {self.description}"




