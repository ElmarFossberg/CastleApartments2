from django.shortcuts import render
from apartment.models import Apartment

# Create your views here.
def index(request):
    apartments = Apartment.objects.all()
    return render(request, 'apartments/apartments.html', {
        "apartments": apartments
    })

def get_apartment_by_id(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    # apartment = [x for x in apartments if x.id = apartment_id][0]
    return render(request, 'apartments/apartment_detail.html', {
        "apartment": apartment
    })