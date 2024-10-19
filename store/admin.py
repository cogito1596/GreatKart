from django.contrib import admin
from .models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "slug",
        "stock",
        "modified_date",
        "is_available",
    )
    list_display_links = ("product_name", "slug")
    list_filter = ("is_available",)
    search_fields = ("product_name", "description")
    prepopulated_fields = {"slug": ("product_name",)}


admin.site.register(Product, ProductAdmin)
