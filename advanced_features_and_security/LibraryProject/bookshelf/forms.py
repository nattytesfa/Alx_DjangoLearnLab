from django import forms
from django.core.exceptions import ValidationError
import html

class ExampleForm(forms.Form):
    """
    Security: Example form demonstrating secure form practices
    Includes validation to prevent XSS and ensure data integrity
    """
    
    # Security: Form fields with proper validation attributes
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'maxlength': '100',  # Security: Client-side length validation
            'pattern': '[A-Za-z\\s]+',  # Security: Basic input pattern
        }),
        help_text="Enter your full name (letters and spaces only)"
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        }),
        help_text="Enter a valid email address"
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message',
            'maxlength': '500',  # Security: Limit message length
        }),
        required=True,
        help_text="Enter your message (maximum 500 characters)"
    )
    
    def clean_name(self):
        """Security: Sanitize and validate name input to prevent XSS"""
        name = self.cleaned_data['name']
        
        # Security: Remove leading/trailing whitespace
        name = name.strip()
        
        # Security: Check for minimum length
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        
        # Security: Check for maximum length
        if len(name) > 100:
            raise ValidationError('Name must not exceed 100 characters.')
        
        # Security: Validate characters (only letters and spaces)
        if not all(c.isalpha() or c.isspace() for c in name):
            raise ValidationError('Name can only contain letters and spaces.')
        
        # Security: Check for dangerous patterns that could indicate XSS
        dangerous_patterns = [
            '<script>', '</script>', 'javascript:', 'onload=', 'onerror=',
            'onclick=', 'vbscript:', '<iframe>', '</iframe>'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in name.lower():
                raise ValidationError('Invalid input detected in name field.')
        
        return name
    
    def clean_message(self):
        """Security: Sanitize and validate message input"""
        message = self.cleaned_data['message']
        
        # Security: Remove leading/trailing whitespace
        message = message.strip()
        
        # Security: Check for minimum length
        if len(message) < 10:
            raise ValidationError('Message must be at least 10 characters long.')
        
        # Security: Check for maximum length
        if len(message) > 500:
            raise ValidationError('Message must not exceed 500 characters.')
        
        # Security: Basic XSS prevention - check for script tags
        dangerous_tags = ['<script>', '</script>', 'javascript:', '<iframe>']
        for tag in dangerous_tags:
            if tag in message.lower():
                # Security: Instead of rejecting, we could sanitize the input
                # For this example, we'll raise a validation error
                raise ValidationError('Message contains potentially unsafe content.')
        
        # Security: Escape HTML characters for safe display
        # In a real scenario, you might use a sanitizer library like bleach
        message = html.escape(message)
        
        return message
    
    def clean(self):
        """Security: Cross-field validation if needed"""
        cleaned_data = super().clean()
        
        # Example of cross-field validation
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        
        if name and email:
            # Security: Additional business logic validation
            # For example, check if name matches email pattern
            pass
        
        return cleaned_data

class SecureBookForm(forms.ModelForm):
    """
    Security: Model form with enhanced security features
    Extends the existing Book model with additional validation
    """
    from .models import Book
    
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '200',  # Security: Input length validation
                'pattern': '[A-Za-z0-9\\s\\-\\.\\,]+',  # Security: Input pattern
            }),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_title(self):
        """Security: Enhanced title validation"""
        title = self.cleaned_data['title']
        
        # Security: Basic sanitization
        title = title.strip()
        
        # Security: Length validation
        if len(title) < 2:
            raise ValidationError('Title must be at least 2 characters long.')
        if len(title) > 200:
            raise ValidationError('Title must not exceed 200 characters.')
        
        # Security: XSS prevention
        dangerous_patterns = ['<script>', '</script>', 'javascript:', 'onload=']
        for pattern in dangerous_patterns:
            if pattern in title.lower():
                raise ValidationError('Title contains potentially unsafe content.')
        
        return title
