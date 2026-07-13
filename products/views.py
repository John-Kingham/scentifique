from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from products.forms import ProductForm

from .models import Colour, Fragrance, Product


class ProductDetail(DetailView):
    model = Product
    template_name = "products/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["colours"] = Colour.objects.all()
        context["fragrances"] = Fragrance.objects.all()
        context["quantities"] = range(1, settings.MAX_LINE_ITEM_QUANTITY + 1)
        return context


class ProductList(ListView):
    context_object_name = "products"
    model = Product
    template_name = "products/products.html"


@login_required
def add_product(request):
    """A view for adding products from the front-end."""

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only admins can add products.")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"{product.name} added.")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request,
                "Failed to add product. Check that the form is valid.",
            )
    else:
        form = ProductForm()
    template = "products/add_product.html"
    context = {"form": form}
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """A view for editing a product."""

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only admins can edit products.")
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated {product.name}.")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request,
                "Failed to update product. Check that the form is valid.",
            )
    else:
        form = ProductForm(instance=product)

    template = "products/edit_product.html"
    context = {"form": form, "product": product}
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """A view for deleting a product."""

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only admins can delete products.")
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)
    product_name = product.name
    product.delete()
    messages.success(request, f"Deleted {product_name}")
    return redirect(reverse("products"))
