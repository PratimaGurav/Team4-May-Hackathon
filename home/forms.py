from .models import Contact
from django import forms

class ContactForm(forms.ModelForm):
    """Form for the contact"""
    class Meta:
        """Meta class"""
        model = Contact
        fields = [
            'name',
            'email',
            'subject',
            'message',
            ]
        widgets = {

        }