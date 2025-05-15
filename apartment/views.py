from django.shortcuts import render
from apartment.models import Apartment, ApartmentImages
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

    return render(request, 'apartments/apartment_detail.html', {
        "apartment": apartment,
        "images": images,
    })
