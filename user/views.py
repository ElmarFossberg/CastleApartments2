from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from user.forms.profile_form import  ProfileForm

from user.models import UserProfile
from user.forms.profile_form import  BuyerForm, SellerForm, RealEstateFirmForm


# Create your views here.

def register(request):
    if request.method == 'POST':
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

def profile(request):
    prof = request.user.userprofile
    form = None

    if prof.user_type == 'buyer':
        if hasattr(prof, 'buyer'):
            form = BuyerForm(request.POST, instance=prof.buyer)
        else:
            form = BuyerForm(request.POST or None)
    elif prof.user_type == 'seller':
        if hasattr(prof, 'seller'):
            form = SellerForm(request.POST or None, instance=prof.seller)
        else:
            form = SellerForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        # Add any redirection or success messages as needed
        return redirect('profile')  # Assuming you want to reload the profile page after saving

    return render(request, 'user/profile.html', {
        'profile': prof,
        'form': form,
    })