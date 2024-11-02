from django.db import models
from django.urls import reverse


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to="photos/products")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey("categories.Category", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def get_url(self):
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


choices = (
    ("size", "size"),
    ("color", "color"),
)


class variationManager(models.Manager):
    def color(self):
        return super(variationManager, self).filter(
            variation_category="color", is_active=True
        )

    def size(self):
        return super(variationManager, self).filter(
            variation_category="size", is_active=True
        )


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=choices)
    variation_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = variationManager()

    def __str__(self):
        return self.variation_value
