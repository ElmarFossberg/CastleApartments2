from django.db import models

# Create your models here.
class Favourites(models.Model):
    apartment: models.ForeignKey = models.ForeignKey('apartment.Apartment', on_delete=models.CASCADE)
    user: models.ForeignKey = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE)