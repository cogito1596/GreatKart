import datetime
from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
from .models import Order


def place_order(request, total=0, quantity=0, cart_items=None):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()

            # Generate order number
            current_date = datetime.datetime.now().strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # Redirect after successful form submission
            return redirect("checkout")
        else:
            # Render the form again with errors if it's invalid
            return redirect("store")

    # If the request is GET, show the form
    form = OrderForm()
    context = {
        "form": form,
        "cart_items": cart_items,
        "grand_total": grand_total,
        "tax": tax,
    }
    return render(request, "templates/checkout.html", context)
