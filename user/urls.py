from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),

    path('login', LoginView.as_view(template_name='user/login.html'), name='login'),

    path('logout', LogoutView.as_view(next_page='apartment-index'), name='logout'),

    path('profile', views.profile, name='profile'),

    path('seller/<int:profile_id>/', views.get_seller_by_id, name='seller_by_id')
]
