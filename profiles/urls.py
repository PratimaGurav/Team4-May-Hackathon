"""Urls for profiles app."""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('<username>/', views.profile, name='profile'),
    path('signup/', views.register, name='signup'),
    path(
        'login/', auth_views.LoginView.as_view(
            template_name='account/login.html',
        ),
        name='login'
    ),
    path(
        'logout/', auth_views.LogoutView.as_view(
            template_name='account/logout.html'
        ),
        name='logout'
    ),
    path('<username>/update/', views.update_profile, name='profile-update'),
    path('<pk>/delete/', views.delete_profile, name='profile-delete'),
]
