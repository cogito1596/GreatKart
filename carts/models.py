from django.db import models
from store.models import Product
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id if self.cart_id else "Unnamed Cart"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField("store.Variation", blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
