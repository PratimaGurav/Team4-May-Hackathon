from django.urls import path
from .views import chatView


urlpatterns = [
    path('', chatView.as_view(), name='chat'),
]