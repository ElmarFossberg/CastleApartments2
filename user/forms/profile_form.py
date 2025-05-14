from django import forms
from django.forms import ModelForm
from user.models import UserProfile, Buyer, Seller, RealEstateFirm

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'id')

class BuyerForm(ModelForm):
    class Meta:
        model = Buyer
        exclude = ('profile',)
        widgets = {
            'postal_code': forms.Select(attrs={'class': 'form-control'}),
        }

class SellerForm(ModelForm):
    class Meta:
        model = Seller
        exclude = ('profile',)

class RealEstateFirmForm(ModelForm):
    class Meta:
        model = RealEstateFirm
        fields = ['firm_name', 'firm_address', 'firm_image']
