from django.contrib import admin
from .models import Product, Variation


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


class VariationAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "variation_category",
        "variation_value",
        "is_active",
    )
    list_editable = ("is_active",)
    list_filter = ("variation_category", "variation_value")
    search_fields = ("variation_category", "variation_value")


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
