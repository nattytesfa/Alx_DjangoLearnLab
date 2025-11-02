# LibraryProject

This Django project serves as the foundation for developing library management applications.

## Project Structure Exploration

### manage.py
- A command-line utility that lets you interact with this Django project
- Used for running server, creating apps, running migrations

### LibraryProject/settings.py
- Configuration for the Django project
- Contains database settings, installed apps, middleware, templates

### LibraryProject/urls.py
- The URL declarations for the project; a "table of contents" of your Django-powered site
- Maps URL patterns to views

### Other Files:
- `wsgi.py`: WSGI configuration for deployment
- `asgi.py`: ASGI configuration for async servers
- `__init__.py`: Makes directory a Python package
