from django.shortcuts import render
from store.models import Product


def home(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "index.html", context)
