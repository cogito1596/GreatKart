from django.db import models
from accounts.models import Account
from store.models import Product, Variation

# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=264)
    payment_method = models.CharField(max_length=264)
    amount_paid = models.FloatField()
    status = models.CharField(max_length=264)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    status = (
        ("Order Received", "Order Received"),
        ("Order Processing", "Order Processing"),
        ("On The Way", "On The Way"),
        ("Order Completed", "Order Completed"),
        ("Order Canceled", "Order Canceled"),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=264)
    first_name = models.CharField(max_length=264)
    last_name = models.CharField(max_length=264)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=264)
    address_line_1 = models.CharField(max_length=264)
    address_line_2 = models.CharField(max_length=264, blank=True)
    country = models.CharField(max_length=264)
    state = models.CharField(max_length=264)
    city = models.CharField(max_length=264)
    order_note = models.TextField()
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=264, choices=status, default="Order Received")
    ip = models.CharField(max_length=264, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
