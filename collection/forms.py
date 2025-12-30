from django import forms

class AddCardForm(forms.Form):
    """
    Form used to add a Magic: The Gathering card to a user's collection.

    Collects the minimum required data to identify an exact card printing
    and the quantity to add.
    """
    set_code = forms.CharField(
        max_length=10,
        label="Set code",
        help_text="Example: sld, mh3, cmm"
    )

    collector_number = forms.CharField(
        max_length=20,
        label="Collector number",
        help_text="Example: 2008, 12a"
    )

    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Quantity"
    )

    purchase_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Purchase price (optional)"
    )