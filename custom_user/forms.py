from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        help_text='Optional. Format: YYYY-MM-DD'
    )
    profile_photo = forms.ImageField(
        required=False,
        help_text='Optional. Upload a profile photo'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'profile_photo', 'password1', 'password2')
