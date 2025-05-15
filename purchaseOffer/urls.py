from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='offers'),
    path('create', views.create, name='offer-create'),

]
