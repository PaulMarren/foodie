from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating the built-in User model fields.
    """
    email = forms.EmailField()  # Explicit email field

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # Fields from Django User model
        # Username is intentionally excluded as it's not changed after creation


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating the custom Profile model fields.
    Handles user-specific profile data separate from authentication details.
    """
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']  # Custom profile fields
