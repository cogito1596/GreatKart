from .models import Cart, CartItem
from .views import _cart_id


from .models import Cart, CartItem


from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    cart_count = 0
    cart_items = None

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, active=True)
    else:
        cart_id = _cart_id(request)
        try:
            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart, active=True)
        except Cart.DoesNotExist:
            cart_items = None

    if cart_items:
        cart_count = sum(item.quantity for item in cart_items)

    return dict(cart_count=cart_count)
