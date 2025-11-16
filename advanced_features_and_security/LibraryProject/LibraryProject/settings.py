"""
Django security settings configuration with CSP
Enhanced security measures for production deployment
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

# ==================== SECURITY SETTINGS ====================

# Security: Cookie settings for production
CSRF_COOKIE_SECURE = True  # Only send CSRF cookie over HTTPS
SESSION_COOKIE_SECURE = True  # Only send session cookie over HTTPS
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
CSRF_COOKIE_SAMESITE = 'Lax'  # CSRF cookie same-site policy

# Security: Browser protection headers
SECURE_BROWSER_XSS_FILTER = True  # Enable XSS filtering in browser
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking by denying frame embedding
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME type sniffing

# Security: Referrer policy to limit information leakage
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Security: Production deployment settings (when DEBUG=False)
if not DEBUG:
    SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS
    SECURE_HSTS_SECONDS = 31536000  # 1 year HSTS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

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
