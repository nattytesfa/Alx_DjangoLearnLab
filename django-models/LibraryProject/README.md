# LibraryProject - Django Library Management System

## Project Overview
This Django project serves as the foundation for developing library management applications.

## Project Structure Exploration

### manage.py
- Command-line utility for Django project interactions
- Used for running server, creating apps, running migrations
- Entry point for administrative tasks

### LibraryProject/settings.py
- Contains all project configuration
- Database settings (SQLite by default)
- Installed apps (admin, auth, contenttypes, sessions, messages, staticfiles)
- Middleware configuration
- Template settings
- Internationalization settings

### LibraryProject/urls.py
- URL dispatcher and routing configuration
- Maps URL patterns to views
- Currently configured with admin path
- Serves as the "table of contents" for the Django-powered site

### LibraryProject/__init__.py
- Empty file that indicates this is a Python package

### LibraryProject/wsgi.py
- Web Server Gateway Interface configuration
- Used for production deployment

### LibraryProject/asgi.py
- Asynchronous Server Gateway Interface configuration
- For async-capable web servers

## Verification
- Development server successfully runs at http://127.0.0.1:8000/
- Default Django welcome page displays correctly
- All migrations applied successfully
