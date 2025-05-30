from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apartment.context import format_apartments
from favourite.models import Favourites
from apartment.models import Apartment
from apartment.models import ApartmentImages
from django.shortcuts import redirect


# Create your views here.

@login_required(login_url='/user/login')
def index(request):
    user_profile = request.user.userprofile

    # Check if user is seller if he is redirect him
    if user_profile.user_type == "seller":
        return redirect('/my-properties')

    if request.method == 'POST':
        # Make sure the user is logged in
        if not request.user.is_authenticated:
            return redirect('/user/login')
        # Get apartment and user info
        apartment_id = request.POST.get('apartment_id')
        user_profile = request.user.userprofile

        # Toggle the favourite
        if apartment_id and user_profile:
            fav, created = Favourites.objects.get_or_create(user=user_profile, apartment_id=apartment_id)
            if not created:
                fav.delete()
        # Return back
        return redirect(request.META.get('HTTP_REFERER', '/'))

    user_id = request.user.userprofile
    # Get apartment IDs from favourites
    apartment_ids = Favourites.objects.filter(user_id=user_id).values_list('apartment_id', flat=True)
    # Get apartments matching those IDs
    apartments = Apartment.objects.filter(id__in=apartment_ids)
    # Format
    format_apartments(apartments)

    return render(request, 'favourite/favourite.html', {'apartments': apartments})