from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'apartments/apartments.html', {
        "data": "none"
    })

def get_apartment_by_id(request, apartment_id):
    # apartment = [x for x in apartments if x.id = apartment_id][0]
    return render(request, 'apartments/apartment_detail.html', {
        "data": apartment_id
    })