from django.db import models

# Create your models here.

class ApartmentType(models.Model):
    type = models.CharField(max_length=255)
    def __str__(self):
        return self.type

class PostalCode(models.Model):
    postal_code = models.CharField(max_length=255, primary_key=True)
    city_name = models.CharField(max_length=255)

    def __str__(self):
        return self.postal_code

class Apartment(models.Model):
    type = models.ForeignKey(ApartmentType, on_delete=models.PROTECT)
    postal_code = models.ForeignKey(PostalCode, on_delete=models.PROTECT, db_column='postal_code')
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    square_meters = models.DecimalField(max_digits=4, decimal_places=0)
    number_of_bathrooms = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    number_of_bedrooms = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    sold = models.BooleanField()
    description = models.TextField(default='')
    listing_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.address}, {self.postal_code}"

class ApartmentImages(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image = models.CharField(max_length=4096)