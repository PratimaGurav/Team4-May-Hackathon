from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# User registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data.get('username') 
            form.save()
            messages.success(
                request,
                f'Your account has been created! You are now able to log in'
            ) 
            return redirect('')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})


# Create profile view to update profile
@login_required
def profile(request, *args, **kwargs):
    user = get_object_or_404(User, username=kwargs['username'])
    user_profile = get_object_or_404(
            Profile,  user=user
        )
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.user_profile
        ) 
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def update_profile(request, *args, **kwargs):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.user_profile
        ) 
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                f'Your profile has been updated successfully!'
            )
            return HttpResponseRedirect(
                reverse('profile', kwargs={'username': request.user})
            )

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profiles/update_profile.html', context)


def delete_profile(request, pk, *args, **kwargs):
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect('home')
    return render(request, "profiles/profile_confirm_delete.html")