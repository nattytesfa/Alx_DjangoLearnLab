# Permissions and Groups Setup

## Overview
This application uses Django's built-in permission system to control access to book management features.

## Groups and Their Permissions

### Viewers Group
- **Permissions**: `can_view_book`
- **Access**: Can view the list of books
- **Cannot**: Create, edit, or delete books

### Editors Group  
- **Permissions**: `can_view_book`, `can_create_book`, `can_edit_book`
- **Access**: Can view, create, and edit books
- **Cannot**: Delete books

### Admins Group
- **Permissions**: `can_view_book`, `can_create_book`, `can_edit_book`, `can_delete_book`
- **Access**: Full access to all book operations

## Setup Instructions

1. **Run migrations** to create permission records:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
