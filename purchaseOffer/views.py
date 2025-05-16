from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from apartment.models import Apartment, ApartmentImages
from purchaseOffer.models import PurchaseOffer
from user.models import UserProfile, Buyer, Seller
from purchaseOffer.forms.purchase_offer_form import PurchaseOfferForm

from django.contrib import messages


@login_required
def index(request):
    # Make sure the user exists
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # handle missing profile if needed
        return render(request, 'error.html', {"message": "No profile found."}, status=404)

    # IF THE REQUEST IS POST (accepting offers)
    if request.method == "POST":
        offer_id = request.POST.get('offer_id')
        if offer_id:
            try:
                offer = PurchaseOffer.objects.get(id=offer_id)
                offer.status = 'accepted'
                offer.save()
                messages.success(request, "Offer accepted successfully.")
            except PurchaseOffer.DoesNotExist:
                messages.error(request, "Offer not found.")

    # IF THE USER IS BUYER RENDER BUYER HTML
    if profile.user_type == 'buyer':
        try:
            buyer = Buyer.objects.get(profile=profile)
        except Buyer.DoesNotExist:
            return render(request, 'error.html', {"message": "You have to complete your profile."}, status=404)

        purchase_offers = PurchaseOffer.objects.filter(buyer=buyer)
        #Formatting price
        for offer in purchase_offers:
            amount = offer.purchase_amount
            if amount == int(amount):
                amount = int(amount)
            offer.formatted_amount = f"{amount:,}".replace(",", ".")

        return render(request, 'offers/offers_buyer.html', {
            'purchase_offers': purchase_offers
        })

    # IF THE USER IS SELLER RENDER SELLER HTML
    elif profile.user_type == 'seller':
        try:
            seller = Seller.objects.get(profile=profile)
        except Seller.DoesNotExist:
            return render(request, 'error.html', {"message": "You have to complete your profile."}, status=404)

        purchase_offers = PurchaseOffer.objects.filter(seller=seller)

        # Format the price for each offer
        for offer in purchase_offers:
            amount = offer.purchase_amount
            if amount == int(amount):
                amount = int(amount)
            offer.formatted_amount = f"{amount:,}".replace(",", ".")

        return render(request, 'offers/offers_seller.html', {
            'purchase_offers': purchase_offers
        })
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
        return render(request, 'error/../templates/error.html', {"message": "You can't make an offer on your own apartment."})
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


@login_required
def cancel(request, offer_id):
    try:
        offer = PurchaseOffer.objects.get(id=offer_id)
        buyer_user = offer.buyer.profile.user
        seller_user = offer.seller.profile.user

        # Only buyer or seller can reject (authorization)
        if request.user == buyer_user or request.user == seller_user:
            offer.status = 'rejected'
            offer.save()
            messages.success(request, "Offer rejected successfully.")
        else:
            messages.error(request, "You are not allowed to cancel this offer.")
    except PurchaseOffer.DoesNotExist:
        messages.error(request, "Offer not found.")
    return redirect('offers')
