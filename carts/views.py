from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product, Variation
from django.http import HttpResponse


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    if request.method == "POST":
        # Collect variations based on the form data
        variations = []
        for key, value in request.POST.items():
            try:
                variation_object = Variation.objects.get(
                    product_id=product_id,
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                )
                variations.append(variation_object)
            except Variation.DoesNotExist:
                pass

        product = get_object_or_404(Product, id=product_id)

        # Get or create cart
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

        # Check for existing cart items with the same product and variations
        cart_items = CartItem.objects.filter(cart=cart, product=product)
        variation_ids = [var.id for var in variations]
        item_found = False

        for cart_item in cart_items:
            existing_variation_ids = list(
                cart_item.variations.values_list("id", flat=True)
            )
            if set(variation_ids) == set(existing_variation_ids):
                # If a matching cart item is found, increment its quantity
                cart_item.quantity += 1
                cart_item.save()
                item_found = True
                break

        # If no matching item was found, create a new cart item
        if not item_found:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
            if variations:
                cart_item.variations.set(variations)
            cart_item.save()

    return redirect(product.get_url())


def decrease_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))

    # Collect selected variations from the request
    variations = []
    for key, value in request.POST.items():
        try:
            variation_object = Variation.objects.get(
                product_id=product_id,
                variation_category__iexact=key,
                variation_value__iexact=value,
            )
            variations.append(variation_object)
        except Variation.DoesNotExist:
            pass

    # Find matching cart item with the specified variations
    cart_items = CartItem.objects.filter(cart=cart, product=product)
    variation_ids = {var.id for var in variations}
    cart_item_found = False

    for cart_item in cart_items:
        existing_variation_ids = set(cart_item.variations.values_list("id", flat=True))
        if variation_ids == existing_variation_ids:
            # Decrease quantity or delete if it's the last one
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
            cart_item_found = True
            break

    if not cart_item_found:
        print("No matching cart item found with the specified variations.")

    return redirect("cart")


def remove_cart(request, product_id, cart_item_id):
    # Find the specific cart item
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart, product=product)
    cart_item.delete()
    return redirect("cart")  # Replace 'cart' with the name of your cart view


def cart(request, total=0, quantity=0):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_objects = CartItem.objects.filter(cart=cart, active=True)
    for item in cart_objects:
        total += item.product.price * item.quantity
        quantity += item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax
    context = {
        "total": round(total, 2),
        "quantity": quantity,
        "cart_objects": cart_objects,
        "grand_total": round(grand_total, 2),
        "tax": round(tax, 2),
    }
    return render(request, "carts/cart.html", context)
