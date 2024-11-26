from django.contrib import admin
from .models import Cart, CartItem


# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ["cart_id", "date_added"]


class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "cart",
        "quantity",
        "active",
        "get_id",
    ]

    def get_id(self, obj):
        return obj.id

    get_id.short_description = "ID"


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
