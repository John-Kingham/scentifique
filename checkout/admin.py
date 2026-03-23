from django.contrib import admin

from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ("total",)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        "order_number",
        "date",
        "delivery",
        "lineitems_total",
        "grand_total",
        "original_cart",
        "stripe_pi_id",
    )

    fields = (
        "order_number",
        "date",
        "full_name",
        "email",
        "phone_number",
        "country",
        "postcode",
        "town_or_city",
        "street_address1",
        "street_address2",
        "county",
        "delivery",
        "lineitems_total",
        "grand_total",
        "original_cart",
        "stripe_pi_id",
    )

    list_display = (
        "order_number",
        "date",
        "full_name",
        "lineitems_total",
        "delivery",
        "grand_total",
    )

    ordering = ("-date",)


admin.site.register(Order, OrderAdmin)
