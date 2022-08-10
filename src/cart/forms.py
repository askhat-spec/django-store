from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 20)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='', widget=forms.Select(attrs={'class': 'form-select'}))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
