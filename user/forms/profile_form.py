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

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')

        if not national_id:
            raise forms.ValidationError("National ID is required.")

        # Check if national_id is exactly 10 digits
        if not national_id.isdigit() or len(national_id) != 10:
            raise forms.ValidationError("National ID must be exactly 10 digits.")

        return national_id

class SellerForm(ModelForm):
    class Meta:
        model = Seller
        exclude = ('profile',)

class RealEstateFirmForm(ModelForm):
    class Meta:
        model = RealEstateFirm
        fields = ['firm_name', 'firm_address', 'firm_image']
