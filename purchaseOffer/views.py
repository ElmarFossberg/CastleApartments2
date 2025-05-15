from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from user.models import UserProfile, Buyer, Seller

@login_required
def index(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # handle missing profile if needed
        return render(request, 'error.html', {"message": "No profile found."})

    if profile.user_type == 'buyer':
        return render(request, 'offers/offers_buyer.html')
    elif profile.user_type == 'seller':
        return render(request, 'offers/offers_seller.html')
    else:
        return render(request, 'error.html', {"message": "Invalid user type."})
