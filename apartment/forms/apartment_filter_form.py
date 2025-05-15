from django import forms
from apartment.models import ApartmentType, PostalCode
SORT_CHOICES = [
    ('date', 'Newest first'),
    ('price_asc', 'Price (low to high)'),
    ('price_desc', 'Price (high to low)'),
]

class ApartmentFilterForm(forms.Form):
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    min_price = forms.IntegerField(required=False, label="Min price")
    max_price = forms.IntegerField(required=False, label="Max price")
    min_square_meters = forms.IntegerField(required=False, label="Min size")
    max_square_meters = forms.IntegerField(required=False, label="Max size")
    type = forms.ModelChoiceField(queryset=ApartmentType.objects.all(), required=False)
    postal_code = forms.ModelChoiceField(queryset=PostalCode.objects.all(), required=False)
    sold = forms.ChoiceField(
        choices=[('', 'Any'), ('true', 'Yes'), ('false', 'No')],
        required=False,
        widget=forms.RadioSelect
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label="Sort by",
        initial="date"
    )
