from apartment.models import ApartmentImages


def user_profile(request):
    if request.user.is_authenticated:
        return {'user_profile': request.user.userprofile}
    return {}

# Formatting apartments
def format_apartments(apartments):
    for apartment in apartments:
        image = ApartmentImages.objects.filter(apartment=apartment).first()
        apartment.image = image.image if image else "https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png"
        apartment.formatted_price = f"{apartment.price:,.0f}".replace(",", ".")
        apartment.number_of_rooms = apartment.number_of_bathrooms + apartment.number_of_bedrooms
        apartment.save()