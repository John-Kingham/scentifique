from django.shortcuts import get_object_or_404, render

from .models import Colour, Fragrance, Product


def all_products(request):
    """A view to show all products."""

    context = {"products": Product.objects.all()}
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """A view to show the details of one product."""

    product = get_object_or_404(Product, pk=product_id)
    colours = Colour.objects.all()
    fragrances = Fragrance.objects.all()
    quantities = range(1, 12+1)
    context = {
        "colours": colours,
        "fragrances": fragrances,
        "quantities": quantities,
        "product": product,
    }
    return render(request, "products/product_detail.html", context)
