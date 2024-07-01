from django.db import models
from datetime import timedelta
from django.utils import timezone

# Create your models here.


STATUS_CHOICES =(
    ("aproved", "aproved"),
    ("rejected", "rejected"),
    ("pending", "pending"),
)

class DirectPayments(models.Model):
    order = models.IntegerField()
    payer_fullname = models.CharField(max_length=100)
    payer_phone = models.CharField(max_length=10)
    payer_address = models.CharField(max_length=100)
    payer_email = models.EmailField()
    shipments = models.IntegerField()
    paid_amount = models.IntegerField()
    total_amount = models.IntegerField()
    date_order_created = models.DateTimeField(auto_now_add=True)  
    status = models.CharField(choices=STATUS_CHOICES, default="pending")
    is_payed = models.BooleanField(default=False)
   
    def save(self, *args, **kwargs):
        if self.date_order_created is None:
            self.date_order_created = timezone.now()
        if self.pk is not None:
            # Prevent changes to date_order_created if it already exists
            original = DirectPayments.objects.get(pk=self.pk)
            self.date_order_created = original.date_order_created
        current_time = timezone.now()
        if not self.is_payed and current_time > self.date_order_created + timedelta(days=3):
            self.status = "rejected"
        elif self.is_payed:
            self.status = "approved"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order#: {self.order}"
    
class MercadoPagoPayment(models.Model):
    merchant_order = models.IntegerField()
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
    iva = models.FloatField(default=0)

    def __str__(self):
        return f"payment: {self.payment_id}"
    

class ItemsPayed(models.Model):
    item_id = models.CharField(max_length=100, default="None")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    direct_payment = models.ForeignKey(DirectPayments, related_name="direct_payment", on_delete=models.CASCADE, null=True)
    mercadopago_payment = models.ForeignKey(MercadoPagoPayment, related_name="mercadopago_payment", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}: {self.description}"




