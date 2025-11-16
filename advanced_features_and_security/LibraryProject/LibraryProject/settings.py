"""
Django HTTPS and Security Configuration
Enhanced security settings for production deployment with HTTPS enforcement
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# Security: DEBUG should be False in production to prevent information leakage
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Security: Define allowed hosts to prevent HTTP Host header attacks
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Security: Add django-csp for Content Security Policy
    'csp',
    'LibraryProject.bookshelf',
    'relationship_app',
]

# Security: Middleware configuration with security protections
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
    # Security: Content Security Policy middleware
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'LibraryProject.LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # Security: Auto-escape by default to prevent XSS
            'autoescape': True,
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.LibraryProject.wsgi.application'

# Database
# Security: Using Django ORM prevents SQL injection by default
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Security: Strong password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Security: Enforce strong passwords
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# ==================== HTTPS & SECURITY SETTINGS ====================

# Security: HTTPS Configuration
# These settings enforce HTTPS connections in production

# SECURE_PROXY_SSL_HEADER: Required when behind a reverse proxy
# Setting: Tuple indicating the header and value that indicate HTTPS
# Impact: Ensures Django correctly detects HTTPS requests from proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURE_SSL_REDIRECT: Redirect all HTTP requests to HTTPS
# Setting: True to enable automatic redirect from HTTP to HTTPS
# Impact: Ensures all traffic uses encrypted HTTPS connections
SECURE_SSL_REDIRECT = not DEBUG  # Enable in production only

# Security: HTTP Strict Transport Security (HSTS)
# HSTS instructs browsers to only connect via HTTPS for specified time

# SECURE_HSTS_SECONDS: Time in seconds for HSTS policy
# Setting: 31536000 = 1 year (recommended for production)
# Impact: Browsers will automatically use HTTPS for this duration
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0  # 1 year in production

# SECURE_HSTS_INCLUDE_SUBDOMAINS: Apply HSTS to all subdomains
# Setting: True to protect all subdomains
# Impact: All subdomains will also require HTTPS
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG

# SECURE_HSTS_PRELOAD: Allow inclusion in browser preload lists
# Setting: True to enable preloading
# Impact: Site can be included in browser HSTS preload lists
SECURE_HSTS_PRELOAD = not DEBUG

# ==================== SECURE COOKIE SETTINGS ====================

# Security: Configure cookies to be sent only over HTTPS

# SESSION_COOKIE_SECURE: Only send session cookies over HTTPS
# Setting: True to prevent session cookies from being sent over HTTP
# Impact: Protects session cookies from being intercepted
SESSION_COOKIE_SECURE = not DEBUG

# CSRF_COOKIE_SECURE: Only send CSRF cookies over HTTPS
# Setting: True to prevent CSRF cookies from being sent over HTTP
# Impact: Protects CSRF tokens from being intercepted
CSRF_COOKIE_SECURE = not DEBUG

# Security: Additional cookie security settings
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
CSRF_COOKIE_SAMESITE = 'Lax'  # CSRF cookie same-site policy

# ==================== SECURITY HEADERS ====================

# Security: Additional HTTP headers for enhanced protection

# X_FRAME_OPTIONS: Clickjacking protection
# Setting: 'DENY' to prevent any framing of the site
# Impact: Protects against clickjacking attacks by denying frame embedding
X_FRAME_OPTIONS = 'DENY'

# SECURE_CONTENT_TYPE_NOSNIFF: Prevent MIME type sniffing
# Setting: True to prevent browsers from interpreting files as different MIME types
# Impact: Reduces risk of XSS attacks through MIME confusion
SECURE_CONTENT_TYPE_NOSNIFF = True

# SECURE_BROWSER_XSS_FILTER: Enable browser XSS filtering
# Setting: True to enable browser's built-in XSS protection
# Impact: Adds an additional layer of XSS protection
SECURE_BROWSER_XSS_FILTER = True

# Security: Referrer policy to limit information leakage
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# ==================== CONTENT SECURITY POLICY (CSP) ====================

# Security: Content Security Policy to prevent XSS attacks
# CSP restricts where resources can be loaded from

CSP_DEFAULT_SRC = ("'self'",)  # Default: only from same origin
CSP_SCRIPT_SRC = ("'self'",)   # Scripts: only from same origin
CSP_STYLE_SRC = ("'self'",)    # Styles: only from same origin
CSP_IMG_SRC = ("'self'", "data:")  # Images: same origin and data URIs
CSP_FONT_SRC = ("'self'",)     # Fonts: only from same origin
CSP_CONNECT_SRC = ("'self'",)  # Connections: only to same origin
CSP_OBJECT_SRC = ("'none'",)   # No embedded objects (Flash, etc.)
CSP_BASE_URI = ("'self'",)     # Base URLs: only same origin
CSP_FRAME_ANCESTORS = ("'none'",)  # No framing (equivalent to X-Frame-Options: DENY)
CSP_FORM_ACTION = ("'self'",)  # Form actions: only to same origin

# Optional: For development, you might need to allow inline styles/scripts
if DEBUG:
    CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
    CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
else:
    # Production: strict policy
    CSP_INCLUDE_NONCE_IN = ['script-src', 'style-src']

# Security: Report CSP violations (optional)
CSP_REPORT_URI = None  # Set to a URL to receive violation reports

# Security: Upgrade insecure requests in production
if not DEBUG:
    CSP_UPGRADE_INSECURE_REQUESTS = True

# ==================== PRODUCTION DEPLOYMENT NOTES ====================

"""
HTTPS Deployment Checklist:

1. Web Server Configuration:
   - Configure Nginx/Apache with SSL certificates
   - Set up SSL termination at the web server level
   - Redirect all HTTP traffic to HTTPS

2. SSL Certificate:
   - Obtain SSL certificate from trusted CA (Let's Encrypt, etc.)
   - Configure certificate paths in web server
   - Set up certificate renewal process

3. Django Settings Verified:
   - DEBUG = False
   - ALLOWED_HOSTS configured with production domain
   - SECURE_SSL_REDIRECT = True
   - All secure cookie settings enabled
   - HSTS settings configured appropriately

4. Testing:
   - Verify HTTPS redirect works
   - Check security headers are present
   - Test that cookies are marked Secure
   - Validate CSP headers
"""



