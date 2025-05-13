from django.shortcuts import render
from apartment.models import Apartment, ApartmentImages


# Create your views here.
def index(request):
    apartments = Apartment.objects.all()
    for apartment in apartments:
        image = ApartmentImages.objects.filter(apartment=apartment).first()
        # Add the first image
        apartment.image = image.image if image else "https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png"
        # Format the price
        apartment.formatted_price = f"{apartment.price:,.0f}".replace(",", ".")
    return render(request, 'apartments/apartments.html', {
        "apartments": apartments
    })

def get_apartment_by_id(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    # apartment = [x for x in apartments if x.id = apartment_id][0]
    return render(request, 'apartments/apartment_detail.html', {
        "apartment": apartment
    })