from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    # If the user is authenticated
    if current_user.is_authenticated:
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

            # Check for existing cart items with the same product and variations
            cart_items = CartItem.objects.filter(user=current_user, product=product)
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
                cart_item = CartItem.objects.create(
                    user=current_user, product=product, quantity=1
                )
                if variations:
                    cart_item.variations.set(variations)
                cart_item.save()
    else:
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
            session_key = _cart_id(request)
            cart, create = Cart.objects.get_or_create(cart_id=session_key)

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
                cart_item = CartItem.objects.create(
                    cart=cart, product=product, quantity=1
                )
                if variations:
                    cart_item.variations.set(variations)
                cart_item.save()

    return redirect("cart")


def decrease_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _cart_id(request)

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
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, product=product)
    else:
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
    # Get the Cart instance

    # Find the specific cart item
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            user=request.user, id=cart_item_id, product=product
        )
    else:
        cart_identifier = _cart_id(request)
        cart = get_object_or_404(Cart, cart_id=cart_identifier)
        cart_item = CartItem.objects.get(cart=cart, id=cart_item_id, product=product)

    # Delete the cart item
    cart_item.delete()
    return redirect("cart")


def cart(request, total=0, quantity=0):
    if request.user.is_authenticated:
        cart_objects = CartItem.objects.filter(user=request.user, active=True)
    else:
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


@login_required(login_url="login")
def checkout(request, total=0, quantity=0, cart_objects=None):
    current_user = request.user
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_objects = CartItem.objects.filter(user=request.user, active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_objects = CartItem.objects.filter(cart=cart, is_active=True)
        tax = (2 * total) / 100
        grand_total = total + tax
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_objects = CartItem.objects.filter(user=current_user, active=True)
        print(cart_objects)
        for item in cart_objects:
            total += item.product.price * item.quantity
            quantity += item.quantity

    except ObjectDoesNotExist:
        pass
    context = {
        "total": round(total, 2),
        "quantity": quantity,
        "cart_objects": cart_objects,
        "grand_total": round(grand_total, 2),
        "tax": round(tax, 2),
    }
    return render(request, "carts/checkout.html", context=context)


# def get_cart(request):
#     if request.user.is_authenticated:
#         print("User is authenticated")

#         # Get the cart for the logged-in user, or create one if it doesn't exist
#         cart = Cart.objects.filter(user=request.user).first()
#         print(f"User cart: {cart.cart_id if cart else None}")

#         if not cart:
#             print("Creating a new cart for the user")
#             cart = Cart.objects.create(user=request.user)

#         # Get the session-based cart ID
#         session_cart_id = _cart_id(request)
#         print(f"Session cart ID: {session_cart_id}")

#         if session_cart_id:
#             try:
#                 # Get the session cart using session_cart_id
#                 session_cart = Cart.objects.get(cart_id=session_cart_id)
#                 print(f"Session cart found: {session_cart.cart_id}")

#                 # Get the cart items from the session cart
#                 session_cart_items = CartItem.objects.filter(cart=session_cart)
#                 print(f"Session cart items: {session_cart_items}")

#                 # Transfer items from the session cart to the logged-in user's cart
#                 # Transfer items from the session cart to the logged-in user's cart
#                 for item in session_cart_items:
#                     # Check if an equivalent cart item already exists
#                     existing_item = CartItem.objects.filter(
#                         user=request.user,
#                         product=item.product,
#                         cart=cart,
#                         variations__in=item.variations.all(),
#                     ).first()
#                     if existing_item:
#                         existing_item.quantity += item.quantity
#                         existing_item.save()
#                     else:
#                         # Create a new item if none exist
#                         CartItem.objects.create(
#                             user=request.user,
#                             product=item.product,
#                             cart=cart,
#                             quantity=item.quantity,
#                             active=True,
#                         )

#                 print(f"Transferred {len(session_cart_items)} items to the user cart")

#                 # Delete the session cart after transferring the items
#                 session_cart.delete()  # This deletes the cart instance from the database
#                 print(f"Session cart {session_cart.cart_id} deleted after transfer.")

#             except Cart.DoesNotExist:
#                 print("No session cart found")
#                 pass
#     else:
#         # If the user is not authenticated, use the session cart
#         cart_id = _cart_id(request)
#         cart, created = Cart.objects.get_or_create(cart_id=cart_id)
#         print(f"Session cart ID: {cart_id}, Cart created: {created}")

#     return cart
