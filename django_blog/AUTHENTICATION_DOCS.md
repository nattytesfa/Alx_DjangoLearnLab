# Django Blog Authentication System Documentation

## Overview
The Django Blog authentication system provides secure user registration, login, logout, and profile management functionality using Django's built-in authentication framework with custom extensions.

## Features

### 1. User Registration
- **URL**: `/register/`
- **Features**:
  - Custom registration form extending `UserCreationForm`
  - Email field with unique validation
  - Password strength validation
  - Automatic login after registration
  - Bootstrap-styled form with validation feedback

### 2. User Login
- **URL**: `/login/`
- **Features**:
  - Django's built-in `LoginView` with custom template
  - Redirect authenticated users away from login page
  - Remember me functionality
  - CSRF protection
  - Secure password handling

### 3. User Logout
- **URL**: `/logout/`
- **Features**:
  - Django's built-in `LogoutView`
  - Confirmation page after logout
  - Automatic redirect to home page
  - Session cleanup

### 4. Profile Management
- **URL**: `/profile/`
- **Features**:
  - View and update user profile
  - Change username, email, first/last name
  - Profile statistics (posts, comments)
  - Link to password change
  - Access to user's posts

### 5. Password Management
- **URL**: `/password-change/`
- **Features**:
  - Secure password change with old password verification
  - Password validation rules
  - Success confirmation page
  - Automatic logout on other devices (if configured)

## Security Features

### CSRF Protection
- All forms include CSRF tokens
- Django's built-in CSRF middleware enabled
- CSRF cookies configured

### Password Security
- Passwords are hashed using PBKDF2 algorithm
- Password validation rules:
  - Minimum 8 characters
  - Cannot be entirely numeric
  - Cannot be too common
  - Cannot be too similar to user information

### Session Management
- Session timeout: 2 weeks
- Browser session persistence
- Secure session cookies (in production)

## File Structure
django_blog/blog/
├── forms.py # Custom authentication forms
├── views.py # Authentication views
├── urls.py # URL configurations
├── templates/blog/ # Authentication templates
│ ├── register.html # Registration page
│ ├── login.html # Login page
│ ├── profile.html # Profile management
│ ├── logout.html # Logout confirmation
│ ├── password_change.html
│ └── password_change_done.html
└── static/blog/css/ # Authentication styles
└── style.css # CSS for auth pages


## Testing Guide

### Manual Testing

1. **Registration Test**:
   ```bash
   # Visit: http://127.0.0.1:8000/register/
   # Test cases:
   - Register with valid information
   - Try duplicate username/email
   - Test password validation
   - Verify auto-login after registration
# Visit: http://127.0.0.1:8000/login/
# Test cases:
- Login with correct credentials
- Login with incorrect credentials
- Test "Remember me" functionality
- Verify redirect after login

# Visit: http://127.0.0.1:8000/profile/ (requires login)
# Test cases:
- Update profile information
- Try duplicate email
- View profile statistics
- Access user's posts

# Visit: http://127.0.0.1:8000/logout/
# Test cases:
- Confirm logout
- Verify session termination
- Check redirect to home
