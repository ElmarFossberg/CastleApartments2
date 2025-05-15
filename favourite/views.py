from django.shortcuts import render

from favourite.models import Favourites
from apartment.models import Apartment
from apartment.models import ApartmentImages


# Create your views here.

def index(request):
    user_id = request.user.id
    # Get apartment IDs from favourites
    apartment_ids = Favourites.objects.filter(user_id=user_id).values_list('apartment_id', flat=True)
    # Get apartments matching those IDs
    apartments = Apartment.objects.filter(id__in=apartment_ids)
    # Format
    for apartment in apartments:
        image = ApartmentImages.objects.filter(apartment=apartment).first()
        # Add the first image
        apartment.image = image.image if image else "https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png"
        # Format the price
        apartment.formatted_price = f"{apartment.price:,.0f}".replace(",", ".")
        apartment.number_of_rooms = apartment.number_of_bathrooms + apartment.number_of_bedrooms
        apartment.save()
    return render(request, 'favourite/favourite.html', {'apartments': apartments})