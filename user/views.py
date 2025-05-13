from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from user.forms.profile_form import  ProfileForm

from user.models import UserProfile


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        return render(request, 'user/register.html', {'form': UserCreationForm()})

def profile(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('profile')

    return render(request, "user/profile.html", {
        'form': ProfileForm(instance=user_profile),
    })