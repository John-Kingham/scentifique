from django.shortcuts import redirect, render


def view_cart(request):
    """A view for the shopping cart page."""
    return render(request, "cart/cart.html")


def add_to_cart(request, product_id):
    """Add items to the cart."""

    colour_id = int(request.POST.get("colour_id"))
    fragrance_id = int(request.POST.get("fragrance_id"))
    quantity = int(request.POST.get("quantity"))
    cart = request.session.get("cart", {})
    order_line_item_key = f"{product_id}_{colour_id}_{fragrance_id}"
    if order_line_item_key in cart:
        cart[order_line_item_key] += quantity
    else:
        cart[order_line_item_key] = quantity
    request.session["cart"] = cart
    print(request.session["cart"])
    return redirect(request.POST.get("redirect_url"))
