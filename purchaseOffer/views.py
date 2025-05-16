from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

import apartment
from apartment.models import Apartment, ApartmentImages, PostalCode
from purchaseOffer.models import *
from user.models import UserProfile, Buyer, Seller

from purchaseOffer.forms.purchase_offer_form import PurchaseOfferForm
from purchaseOffer.forms.finalization_form import ContactInfoForm, PaymentOptionForm, CreditCardForm, BankTransferForm, MortgageForm

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

        purchase_offers = PurchaseOffer.objects.filter(buyer=buyer, finalized=False)
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

        purchase_offers = PurchaseOffer.objects.filter(seller=seller, finalized=False)

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

    try:
        apartment = Apartment.objects.get(id=apartment_id)
    except Apartment.DoesNotExist:
        return render(request, 'error.html', {"message": "Apartment not found."})

    try:
        buyer = Buyer.objects.get(profile__user=request.user)
    except Buyer.DoesNotExist:
        return render(request, 'Error.html', {"message": "Complete your profile first."})

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

def finalize_purchase(request, offer_id):
    step = int(request.GET.get('step', 1))

    purchase_offer = get_object_or_404(PurchaseOffer, id=offer_id)

    form_data = request.session.get('form_data', {})

    if request.method == 'POST':
        if step == 1:
            form = ContactInfoForm(request.POST)
            if form.is_valid():
                contact = form.cleaned_data.copy()
                contact['contact_country'] = contact['contact_country'].name
                contact['contact_postal_code'] = contact['contact_postal_code'].postal_code
                form_data['contact'] = contact
                request.session['form_data'] = form_data
                return redirect(f"{reverse('finalize_purchase', args=[offer_id])}?step=2")

        elif step == 2:
            form = PaymentOptionForm(request.POST)
            if form.is_valid():
                form_data['payment_option'] = form.cleaned_data['payment_option']
                request.session['form_data'] = form_data
                return redirect(f"{reverse('finalize_purchase', args=[offer_id])}?step=3")

        elif step == 3:
            payment_option = form_data.get('payment_option')
            if payment_option == 'credit_card':
                form = CreditCardForm(request.POST)
            elif payment_option == 'bank_transfer':
                form = BankTransferForm(request.POST)
            elif payment_option == 'mortgage':
                form = MortgageForm(request.POST)
            else:
                form = None

            if form and form.is_valid():
                form_data['payment_details'] = form.cleaned_data
                request.session['form_data'] = form_data
                return redirect(f"{reverse('finalize_purchase', args=[offer_id])}?step=4")

        elif step == 4:
            if 'confirm' in request.POST:
                payment_option = form_data['payment_option']
                payment_details = form_data['payment_details']

                if payment_option == 'credit_card':
                    credit_card = CreditCard.objects.create(**payment_details)
                    bank_transfer = mortgage = None
                elif payment_option == 'bank_transfer':
                    bank_transfer = BankTransfer.objects.create(**payment_details)
                    credit_card = mortgage = None
                elif payment_option == 'mortgage':
                    mortgage = Mortgage.objects.create(**payment_details)
                    credit_card = bank_transfer = None
                # Create finalized offer
                contact = form_data['contact']
                FinalizedPurchaseOffer.objects.create(
                    purchase_offer=purchase_offer,
                    contact_address=contact['contact_address'],
                    contact_street=contact['contact_street'],
                    contact_city=contact['contact_city'],
                    postal_code=PostalCode.objects.get(postal_code=contact['contact_postal_code']),
                    contact_country=Country.objects.get(name=contact['contact_country']),
                    contact_national_id=contact['contact_national_id'],
                    payment_option=payment_option,
                    credit_card=credit_card,
                    bank_transfer=bank_transfer,
                    mortgage=mortgage,
                    confirmed=True,
                    confirmation_date=timezone.now()
                )
                purchase_offer.finalized = True
                purchase_offer.save()

                apartment = purchase_offer.apartment
                apartment.sold = True
                apartment.save()

                # Clear session data
                request.session.pop('form_data', None)
                return redirect(f"{reverse('finalize_purchase', args=[offer_id])}?step=5")

    else:
        # GET request: prepare forms with initial data if available
        if step == 1:
            form = ContactInfoForm(initial=form_data.get('contact'))
        elif step == 2:
            form = PaymentOptionForm(initial={'payment_option': form_data.get('payment_option')})
        elif step == 3:
            payment_option = form_data.get('payment_option')
            if payment_option == 'credit_card':
                form = CreditCardForm(initial=form_data.get('payment_details'))
            elif payment_option == 'bank_transfer':
                form = BankTransferForm(initial=form_data.get('payment_details'))
            elif payment_option == 'mortgage':
                form = MortgageForm(initial=form_data.get('payment_details'))
            else:
                form = None
        elif step == 4 or step == 5:
            form = None
        else:
            form = None

    context = {
        'step': step,
        'steps': [1, 2, 3, 4, 5],
        'form': form,
        'form_data': form_data,
        'offer_id': offer_id,
    }

    return render(request, 'offers/finalize_purchase.html', context)