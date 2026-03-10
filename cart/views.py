from django.shortcuts import render


def view_cart(request):
    """A view for the shopping cart page."""
    return render(request, "cart/cart.html")
