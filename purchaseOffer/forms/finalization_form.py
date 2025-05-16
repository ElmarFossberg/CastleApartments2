import re

from django import forms

from apartment.models import PostalCode
from purchaseOffer.models import *
from django.utils import timezone
from datetime import datetime, timedelta


# Contact Info
class ContactInfoForm(forms.Form):
    contact_country = forms.ModelChoiceField(queryset=Country.objects.all())
    contact_national_id = forms.CharField(max_length=20)
    contact_postal_code = forms.ModelChoiceField(queryset=PostalCode.objects.all())
    contact_address = forms.CharField(max_length=255)
    contact_street = forms.CharField(max_length=255)
    contact_city = forms.CharField(max_length=100)

    def clean_contact_national_id(self):
        national_id = self.cleaned_data.get('contact_national_id')
        if not national_id:
            raise forms.ValidationError("National ID is required.")
        if not national_id.isdigit() or len(national_id) != 10:
            raise forms.ValidationError("National ID must be exactly 10 digits.")
        return national_id


# Payment Options
class PaymentOptionForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mortgage', 'Mortgage'),
    ]
    payment_option = forms.ChoiceField(choices=PAYMENT_CHOICES)

# Option 1: Credit Card
class CreditCardForm(forms.Form):
    cardholder_name = forms.CharField(max_length=100)
    credit_card_number = forms.CharField(max_length=20)
    expiry_date = forms.CharField(max_length=5)
    cvc = forms.CharField(max_length=4)

    def clean_credit_card_number(self):
        card_number = self.cleaned_data.get('credit_card_number', '').replace(' ', '')
        if not card_number.isdigit():
            raise forms.ValidationError("Credit card number must contain only digits.")
        # Luhns Algorithm: https://dev.to/seraph776/validate-credit-card-numbers-using-python-37j9
        card_number = [int(num) for num in card_number]
        # 2. Remove the last digit:
        checkDigit = card_number.pop(-1)
        # 3. Reverse the remaining digits:
        card_number.reverse()
        # 4. Double digits at even indices
        card_number = [num * 2 if idx % 2 == 0
                       else num for idx, num in enumerate(card_number)]
        # 5. Subtract 9 at even indices if digit is over 9
        # (or you can add the digits)
        card_number = [num - 9 if idx % 2 == 0 and num > 9
                       else num for idx, num in enumerate(card_number)]
        # 6. Add the checkDigit back to the list:
        card_number.append(checkDigit)
        # 7. Sum all digits:
        checkSum = sum(card_number)
        # 8. If checkSum is divisible by 10, it is valid.
        if checkSum % 10 != 0:
            raise forms.ValidationError("Credit card number is invalid.")
        return self.cleaned_data.get('credit_card_number')

    def clean_expiry_date(self):
        expiration_date = self.cleaned_data.get('expiry_date')
        try:
            exp = datetime.strptime(expiration_date, '%m/%y')
            next_month = exp.replace(day=28) + timedelta(days=4)  # always next month
            last_day = next_month - timedelta(days=next_month.day)
            exp = exp.replace(day=last_day.day, hour=23, minute=59, second=59)
        except ValueError:
            raise forms.ValidationError("Expiry date must be in MM/YY format.")
        if exp < timezone.now().replace(tzinfo=None):
            raise forms.ValidationError("Expiration date has passed.")
        return expiration_date

    def clean_cvc(self):
        cvc = self.cleaned_data.get('cvc')
        if not cvc.isdigit() or len(cvc) not in [3, 4]:
            raise forms.ValidationError("CVC must be 3 or 4 digits.")
        return cvc


# Option 2: Bank
class BankTransferForm(forms.Form):
    bank_account = forms.CharField(max_length=50)

    def clean_bank_account(self):
        account = self.cleaned_data.get('bank_account', '').strip()
        # Icelandic bank format (4 digits - 2 digits - 6 digits)
        icelandic_pattern = r'^\d{4}-\d{2}-\d{6}$'
        if not re.match(icelandic_pattern, account):
            raise forms.ValidationError("Bank account must follow the Icelandic bank format (4 digits - 2 digits - 6 digits).")
        return account



# Option 3: Mortgage
class MortgageForm(forms.Form):
    PROVIDER_CHOICES = Mortgage.PROVIDER_CHOICES
    provider = forms.ChoiceField(choices=PROVIDER_CHOICES)
