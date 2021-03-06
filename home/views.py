"""
Django settings for views.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views import View
from chat.models import Chat
from .models import Contact
from .forms import ContactForm
from django.views.generic.edit import FormView


# Create your views here.
class HomeView(View):
    """ Class to set home page view settings """
    def get(self, request, *args, **kwargs):
        """ Function to set home page view settings """
        chat = Chat.objects.all()
        return render(request, 'index.html', {'chat': chat})


# class ContactView(View):
#     """ Class to set contact page view settings """
#     def get(self, request, *args, **kwargs):
#         """ Function to set contact page view settings """
#         chat = Chat.objects.all()
#         return render(request, 'contact-us.html', {})


class ContactView(View):
    template_name = 'contact-us.html'
    form_class = ContactForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # save form data
            form.save()
            messages.success(self.request, 'Thank You, your form submission has been successful!!')
            return HttpResponseRedirect('/')
        else:
            errors = form.errors
            for error in errors:
                messages.error(self.request, 'Please, enter valid ' + error)
            # print form.errors
            print(form.errors)
            return render(request, self.template_name, {'form': form})
