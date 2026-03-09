from django.contrib import admin
from .models import Colour, Fragrance, Product


@admin.register(Colour)
class ColourAdmin(admin.ModelAdmin):
    ordering = ("name",)


@admin.register(Fragrance)
class FragranceAdmin(admin.ModelAdmin):
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "image")
    ordering = ("name",)
