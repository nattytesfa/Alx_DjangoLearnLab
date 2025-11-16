from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Book

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Required. Format: YYYY-MM-DD'
    )
    profile_photo = forms.ImageField(
        required=False,
        help_text='Optional. Upload a profile photo'
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'date_of_birth', 'profile_photo', 'password1', 'password2')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }
