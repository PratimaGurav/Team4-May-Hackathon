from django.urls import path
from .views import HomeView, profile_view


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile/', profile_view, name='user-profile'),
]
