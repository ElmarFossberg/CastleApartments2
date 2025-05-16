from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='offers'),
    path('create', views.create, name='offer-create'),

    path('<int:offer_id>/cancel/', views.cancel, name='offer-cancel'),
    path('finalize_purchase/<int:offer_id>/', views.finalize_purchase, name='finalize_purchase'),

]
