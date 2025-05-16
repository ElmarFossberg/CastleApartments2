from django.db import models
from django.utils import timezone
# Create your models here.



# Offer
class PurchaseOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    apartment = models.ForeignKey('apartment.Apartment', on_delete=models.CASCADE)
    buyer = models.ForeignKey('user.Buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey('user.Seller', on_delete=models.CASCADE)
    expiration_date = models.DateTimeField()
    purchase_date = models.DateTimeField(default=timezone.now)
    purchase_amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    finalized = models.BooleanField(default=False)

# Payment methods
class CreditCard(models.Model):
    cardholder_name = models.CharField(max_length=100)
    credit_card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=5)
    cvc = models.CharField(max_length=4)

class BankTransfer(models.Model):
    bank_account = models.CharField(max_length=50)

class Mortgage(models.Model):
    PROVIDER_CHOICES = [
        ('arion', 'Arion banki'),
        ('landsbankinn', 'Landsbankinn'),
        ('islandsbanki', 'Íslandsbanki'),
    ]
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# The FINAL
class FinalizedPurchaseOffer(models.Model):
    purchase_offer = models.OneToOneField(PurchaseOffer, on_delete=models.CASCADE)
    contact_address = models.CharField(max_length=255)
    contact_street = models.CharField(max_length=255)
    contact_city = models.CharField(max_length=100)
    postal_code = models.ForeignKey('apartment.PostalCode', on_delete=models.SET_NULL, null=True)
    contact_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    contact_national_id = models.CharField(max_length=20)

    payment_option = models.CharField(max_length=20, choices=(
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mortgage', 'Mortgage'),
    ))

    credit_card = models.OneToOneField(CreditCard, null=True, blank=True, on_delete=models.SET_NULL)
    bank_transfer = models.OneToOneField(BankTransfer, null=True, blank=True, on_delete=models.SET_NULL)
    mortgage = models.OneToOneField(Mortgage, null=True, blank=True, on_delete=models.SET_NULL)

    confirmed = models.BooleanField(default=False)
    confirmation_date = models.DateTimeField(blank=True, null=True)





