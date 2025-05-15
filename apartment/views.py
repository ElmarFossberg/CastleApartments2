from django.shortcuts import render
from apartment.models import Apartment, ApartmentImages
from user.models import Seller, Buyer
from favourite.models import Favourites
from purchaseOffer.models import PurchaseOffer
from .forms.apartment_filter_form import ApartmentFilterForm


# Create your views here.
def index(request):
    #Get the forms
    form = ApartmentFilterForm(request.GET)
    apartments = Apartment.objects.all()

    if form.is_valid():
        #shorthand
        cd = form.cleaned_data

        # Apply filters
        if cd['address']:
            apartments = apartments.filter(address__icontains=cd['address'])
        if cd['min_price']:
            apartments = apartments.filter(price__gte=cd['min_price'])
        if cd['max_price']:
            apartments = apartments.filter(price__lte=cd['max_price'])
        if cd['min_square_meters']:
            apartments = apartments.filter(square_meters__gte=cd['min_square_meters'])
        if cd['max_square_meters']:
            apartments = apartments.filter(square_meters__lte=cd['max_square_meters'])
        if cd['type']:
            apartments = apartments.filter(type=cd['type'])
        if cd['postal_code']:
            apartments = apartments.filter(postal_code=cd['postal_code'])
        if cd['sold'] != '':
            apartments = apartments.filter(sold=(cd['sold'] == 'true'))

        # Sorting
        sort = cd.get('sort')
        if sort == 'price_asc':
            apartments = apartments.order_by('price')
        elif sort == 'price_desc':
            apartments = apartments.order_by('-price')
        elif sort == 'date':
            apartments = apartments.order_by('-listing_date')
        else:
            apartments = apartments.order_by('-listing_date', 'sold')  # default

    # Format
    for apartment in apartments:
        image = ApartmentImages.objects.filter(apartment=apartment).first()
        apartment.image = image.image if image else "https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png"
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
    purchase_offer = None
    seller_profile = None

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
            # Get purchase offer info
            try:
                purchase_offer = PurchaseOffer.objects.get(buyer=buyer, apartment=apartment)
            except PurchaseOffer.DoesNotExist:
                purchase_offer = None
        # Get seller info
        try:
            seller = Seller.objects.get(id=apartment.seller_id)
            seller_profile = seller.profile
        except Seller.DoesNotExist:
            seller_profile = None

    return render(request, 'apartments/apartment_detail.html', {
        "apartment": apartment,
        "images": images,
        "user_type": user_type,
        "seller_profile": seller_profile,
        "purchase_offer": purchase_offer,
    })