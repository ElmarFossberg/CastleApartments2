from django.shortcuts import render
from apartment.models import Apartment, ApartmentImages
from user.models import Seller, Buyer
from favourite.models import Favourites
from purchaseOffer.models import PurchaseOffer
from .forms.apartment_filter_form import ApartmentFilterForm


# Create your views here.
def index(request):
    #Get the Form
    form = ApartmentFilterForm(request.GET)
    #Get all apartments
    apartments = Apartment.objects.all()

    if form.is_valid():
        # Apply filters
        if form.cleaned_data['address']:
            apartments = apartments.filter(address__icontains=form.cleaned_data['address'])
        if form.cleaned_data['min_price']:
            apartments = apartments.filter(price__gte=form.cleaned_data['min_price'])
        if form.cleaned_data['max_price']:
            apartments = apartments.filter(price__lte=form.cleaned_data['max_price'])
        if form.cleaned_data['min_square_meters']:
            apartments = apartments.filter(square_meters__gte=form.cleaned_data['min_square_meters'])
        if form.cleaned_data['max_square_meters']:
            apartments = apartments.filter(square_meters__lte=form.cleaned_data['max_square_meters'])
        if form.cleaned_data['type']:
            apartments = apartments.filter(type=form.cleaned_data['type'])
        if form.cleaned_data['postal_code']:
            apartments = apartments.filter(postal_code=form.cleaned_data['postal_code'])
        if form.cleaned_data['sold'] != '':
            apartments = apartments.filter(sold=(form.cleaned_data['sold'] == 'true'))

    #Sorting
    apartments = apartments.order_by('-listing_date', 'sold')

    #Format
    for apartment in apartments:
        image = ApartmentImages.objects.filter(apartment=apartment).first()
        # Add the first image
        apartment.image = image.image if image else "https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png"
        # Format the price
        apartment.formatted_price = f"{apartment.price:,.0f}".replace(",", ".")
        apartment.number_of_rooms = apartment.number_of_bathrooms + apartment.number_of_bedrooms
        apartment.save()
    return render(request, 'apartments/apartments.html', {
        "apartments": apartments,
        "form": form
    })


def get_apartment_by_id(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)

    # Format price
    apartment.formatted_price = f"{apartment.price:,.0f}".replace(",", ".")

    # Get all images for this apartment
    images = ApartmentImages.objects.filter(apartment=apartment)

    # Default values
    apartment.is_favourited = False
    apartment.already_has_purchase_offer = False
    user_type = None

    # Make sure the app dosent crash if user is not logged in
    if request.user.is_authenticated:
        # Get the user info
        user_profile = request.user.userprofile
        user_type = user_profile.user_type

        # Check if user is buyer
        try:
            buyer = Buyer.objects.get(profile=user_profile)
        except Buyer.DoesNotExist:
            buyer = None

        # Check if favourited
        apartment.is_favourited = Favourites.objects.filter(
            user=user_profile,
            apartment=apartment
        ).exists()
        # If user is a buyer does he already have an offer?
        if buyer:
            apartment.already_has_purchase_offer = PurchaseOffer.objects.filter(
                buyer=buyer,
                apartment=apartment
            ).exists()

        # Get seller info
        seller = Seller.objects.get(id=apartment.seller_id)
        seller_profile = seller.profile  # This is the UserProfile instance

    return render(request, 'apartments/apartment_detail.html', {
        "apartment": apartment,
        "images": images,
        "user_type": user_type,
        "seller_profile": seller_profile,
    })