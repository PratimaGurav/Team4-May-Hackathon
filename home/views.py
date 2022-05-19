from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View

# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home/home.html', {})


# Create profile view
@login_required
def profile_view(request):
    return render(request, 'home/profile.html')