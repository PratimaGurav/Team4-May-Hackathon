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
            'name': forms.TextInput(attrs={'required': True}),
            'email': forms.TextInput(attrs={'required': True}),
            'subject': forms.TextInput(attrs={'required': True}),
            'message': forms.TextInput(attrs={'required': True}),

        }