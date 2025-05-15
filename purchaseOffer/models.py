from django.db import models
from django.utils import timezone

# Create your models here.
class PurchaseOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('contingent', 'Contingent'),
    ]

    apartment = models.ForeignKey('apartment.Apartment', on_delete=models.CASCADE)
    buyer = models.ForeignKey('user.Buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey('user.Seller', on_delete=models.CASCADE)
    expiration_date = models.DateTimeField()
    purchase_date = models.DateTimeField(default=timezone.now)
    purchase_amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

