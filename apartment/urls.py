from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='apartment-index'),

    path('<int:apartment_id>', views.get_apartment_by_id, name='apartment_by_id' ),

    path('my-properties', views.my_properties, name='my_properties'),

]