from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "full_name",
            "email",
            "phone_number",
            "street_address1",
            "street_address2",
            "town_or_city",
            "postcode",
            "country",
            "county",
        )

    def __init__(self, *args, **kwargs):
        """Initialise the order form."""

        super().__init__(*args, **kwargs)
        placeholders = self._placeholders()
        for field_name, field in self.fields.items():
            field.label = False
            placeholder = placeholders.get(field_name)
            if placeholder:
                if field.required:
                    placeholder += " *"
                field.widget.attrs["placeholder"] = placeholder

    def _placeholders(self):
        """Return form field placeholders."""

        return {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone_number": "Phone Number",
            "street_address1": "Street Address 1",
            "street_address2": "Street Address 2",
            "town_or_city": "Town or City",
            "county": "County, State or Locality",
            "postcode": "Postal Code",
            "country": "Country",
        }
