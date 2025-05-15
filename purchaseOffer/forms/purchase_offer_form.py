from django import forms
from django.forms import ModelForm
from purchaseOffer.models import PurchaseOffer
from django.utils import timezone


class PurchaseOfferForm(ModelForm):
    class Meta:
        model = PurchaseOffer
        exclude = ['apartment', 'buyer', 'seller', 'status', 'purchase_date']

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        if expiration_date and expiration_date.date() <= timezone.now().date():
            raise forms.ValidationError("Expiration date must be in the future.")
        return expiration_date

    def clean_purchase_amount(self):
        purchase_amount = self.cleaned_data.get('purchase_amount')
        if purchase_amount <= 0:
            raise forms.ValidationError("Purchase amount must be positive.")
        return purchase_amount
