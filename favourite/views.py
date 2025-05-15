from django.shortcuts import render

from favourite.models import Favourites
from apartment.models import Apartment
from apartment.models import ApartmentImages
from django.shortcuts import redirect


# Create your views here.

def index(request):
    if request.method == 'POST':
        # example: get apartment id from POST data
        apartment_id = request.POST.get('apartment_id')
        user_profile = request.user.userprofile  # get UserProfile instance

        # create a favourite if it doesn't exist
        if apartment_id and user_profile:
            fav, created = Favourites.objects.get_or_create(user=user_profile, apartment_id=apartment_id)
            if not created:
                # If favourite already exists, remove it (unfavourite)
                fav.delete()

        # then redirect or continue to show updated list
        return redirect(request.META.get('HTTP_REFERER', '/'))

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