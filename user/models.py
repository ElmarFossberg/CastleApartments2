from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    profile_image = models.TextField(max_length=4096)

    def __str__(self):
        return self.full_name

class Buyer(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    postal_code = models.ForeignKey('apartment.PostalCode', on_delete=models.PROTECT, db_column='postal_code')
    national_id = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.profile.full_name

class RealEstateFirm(models.Model):
    firm_name = models.CharField(max_length=100)
    postal_code = models.ForeignKey('apartment.PostalCode', on_delete=models.PROTECT, db_column='postal_code', default=101)
    firm_address = models.CharField(max_length=255)
    firm_image = models.TextField(max_length=4096)

    def __str__(self):
        return self.firm_name


class Seller(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    firm = models.ForeignKey(RealEstateFirm, null=True, blank=True, on_delete=models.SET_NULL)
    cover_image = models.CharField(max_length=4096, null=True, blank=True)
    bio = models.TextField(max_length=4096, default=None, null=True, blank=True)

    def __str__(self):
        return self.profile.full_name

