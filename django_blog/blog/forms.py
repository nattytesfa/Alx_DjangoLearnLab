from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from taggit.forms import TagWidget
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'tags': TagWidget(),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError('Title cannot be empty.')
        if len(title) < 5:
            raise ValidationError('Title should be at least 5 characters long.')
        if len(title) > 200:
            raise ValidationError('Title cannot exceed 200 characters.')
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise ValidationError('Content cannot be empty.')
        if len(content) < 10:
            raise ValidationError('Content should be at least 10 characters long.')
        return content


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments.
    """
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'maxlength': '1000'
            }),
            'parent': forms.HiddenInput(),  # Hidden field for parent comment ID
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove parent field from display in regular comment form
        self.fields['parent'].required = False
        
    def clean_content(self):
        """
        Validate comment content.
        """
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise ValidationError('Comment cannot be empty.')
        if len(content) < 5:
            raise ValidationError('Comment should be at least 5 characters long.')
        if len(content) > 1000:
            raise ValidationError('Comment cannot exceed 1000 characters.')
        return content


class CommentEditForm(forms.ModelForm):
    """
    Form for editing existing comments.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': '1000'
            }),
        }
    
    def clean_content(self):
        """
        Validate comment content.
        """
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise ValidationError('Comment cannot be empty.')
        if len(content) < 5:
            raise ValidationError('Comment should be at least 5 characters long.')
        if len(content) > 1000:
            raise ValidationError('Comment cannot exceed 1000 characters.')
        return content


class UserRegisterForm(UserCreationForm):
    """
    Custom registration form extending Django's UserCreationForm.
    Adds email field and custom validation.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['username', 'email']:  # Already styled
                field.widget.attrs['class'] = 'form-control'
                if field_name == 'password1':
                    field.widget.attrs['placeholder'] = 'Create a password'
                elif field_name == 'password2':
                    field.widget.attrs['placeholder'] = 'Confirm password'
    
    def clean_email(self):
        """
        Validate that the email is unique.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email


class UserLoginForm(AuthenticationForm):
    """
    Custom login form with Bootstrap styling.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Enter your username'
            elif field_name == 'password':
                field.widget.attrs['placeholder'] = 'Enter your password'


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name (optional)'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name (optional)'
            }),
        }
    
    def clean_email(self):
        """
        Validate that the email is unique, excluding current user.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This email is already registered.')
        return email
