from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages

from apartment.models import Apartment
from user.forms.profile_form import  ProfileForm

from user.models import UserProfile, Seller, RealEstateFirm
from user.forms.profile_form import  BuyerForm, SellerForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def register(request):
    if request.method == 'POST':
        # Get the forms: Django's built-in user form and our custom profile form
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user (the user will be linked to the profile)
            user = user_form.save()

            # Save the profile with the user linked
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Create the specific model (Buyer or Seller)
            if profile.user_type == 'buyer':
                buyer_form = BuyerForm(request.POST)
                if buyer_form.is_valid():
                    buyer = buyer_form.save(commit=False)
                    buyer.profile = profile  # Link to the UserProfile
                    buyer.save()

            elif profile.user_type == 'seller':
                seller_form = SellerForm(request.POST)
                if seller_form.is_valid():
                    seller = seller_form.save(commit=False)
                    seller.profile = profile  # Link to the UserProfile
                    seller.save()

            return redirect('login')  # Redirect to login page after successful registration

    else:
        # Empty forms for GET request
        user_form = UserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'user/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def profile(request):
    # Get access to the profile and initilize the form
    prof = request.user.userprofile
    form = None
    # If the account is a buyer the profile will show the buyer form
    if prof.user_type == 'buyer':
        if hasattr(prof, 'buyer'):
            form = BuyerForm(request.POST or None, instance=prof.buyer)
        else:
            form = BuyerForm(request.POST or None)
    # If the account is a seller the profile will show the buyer form
    elif prof.user_type == 'seller':
        if hasattr(prof, 'seller'):
            form = SellerForm(request.POST or None, instance=prof.seller)
        else:
            form = SellerForm(request.POST or None)
    # SIDE NOTE: It should be impossible to be neither so else is not needed

    # Code to update the profile through POST method
    success = False
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        if not hasattr(prof, prof.user_type):  # if buyer/seller does not exist yet
            obj.profile = prof
        obj.save()
        success = True

    # Render the html and send relevant data
    return render(request, 'user/profile.html', {
        'profile': prof,
        'form': form,
        "success": success,
    })

def get_seller_by_id(request, profile_id):
    profile = UserProfile.objects.get(id=profile_id)
    seller = Seller.objects.get(profile=profile)
    apartments = Apartment.objects.filter(seller=seller)  # use filter, not get
    seller_profile = seller.profile
    try:
        real_estate_firm = RealEstateFirm.objects.get(seller=seller)
    except RealEstateFirm.DoesNotExist:
        real_estate_firm = None

    return render(request, 'user/seller.html', {
        "apartments": apartments,
        "seller": seller,
        "seller_profile": seller_profile,
        "real_estate_firm": real_estate_firm,
    })