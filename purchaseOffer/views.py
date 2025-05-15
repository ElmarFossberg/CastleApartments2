from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from apartment.models import Apartment, ApartmentImages
from user.models import UserProfile, Buyer, Seller
from purchaseOffer.forms.purchase_offer_form import PurchaseOfferForm

@login_required
def index(request):
    # Make sure the user exissts
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # handle missing profile if needed
        return render(request, 'error.html', {"message": "No profile found."})
    # Show relevant html based on user_type
    if profile.user_type == 'buyer':
        return render(request, 'offers/offers_buyer.html')
    elif profile.user_type == 'seller':
        return render(request, 'offers/offers_seller.html')
    else:
        return render(request, 'error.html', {"message": "Invalid user type."})

@login_required
def create(request):
    # Access the data needed to keep going
    apartment_id = request.GET.get('apartment_id')
    apartment = get_object_or_404(Apartment, id=apartment_id)
    buyer = get_object_or_404(Buyer, profile__user=request.user)
    seller = apartment.seller

    # Make sure the apartment is not owned by the owner
    if apartment.seller.profile.user == request.user:
        return render(request, 'error.html', {"message": "You can't make an offer on your own apartment."})
    # Standard POST
    if request.method == 'POST':
        form = PurchaseOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.apartment = apartment
            offer.buyer = buyer
            offer.seller = seller
            offer.save()
            return redirect('offers')
    else:
        form = PurchaseOfferForm()

    # This is getting data for the apartment display (copied from apartments.view)
    image = ApartmentImages.objects.filter(apartment=apartment).first()
    apartment.image = image.image if image else "https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png"
    apartment.formatted_price = f"{apartment.price:,.0f}".replace(",", ".")
    apartment.number_of_rooms = apartment.number_of_bathrooms + apartment.number_of_bedrooms

    return render(request, 'offers/create_offer.html', {
        'form': form,
        'apartment': apartment,
    })
