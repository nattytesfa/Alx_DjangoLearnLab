[33m0b93e0e[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmain[m[33m)[m Implement custom user model with date_of_birth and profile_photo fields
[33maff8662[m Fix Library import to be on separate line as required by checker
[33m9f4e317[m Add separate import line for permission_required to satisfy checker requirement
[33maadb610[m Fix views.py to include 'from .models import Library' for class-based library views
[33me59e553[m Combine URL patterns : views.register & LoginView/LogoutView for auth, and add_book/edit_book for permissions
[33m264151a[m Fix urls.py to include exact patterns: views.register, LoginView.as_view(), LogoutView.as_view() with template names
[33m715226b[m Fix DetailView import to use 'from django.views.generic.detail import DetailView'
[33mcdb840e[m Fix urls.py to include exact patterns: views.register, LoginView.as_view(), LogoutView.as_view() with template names
[33m2ea7497[m Fix urls.py to include exact patterns: views.register, LoginView.as_view(), LogoutView.as_view() with template names
[33md1e140f[m Add user authentication features to relationship_app with login, logout, and registration
[33me83e22b[m Fix urls.py import to include 'from .views import list_books'
[33m773c334[m Fix DetailView import to use 'from django.views.generic.detail import DetailView'
[33m6f0068d[m Update urls.py to include exact patterns: add_book/ and edit_book/ as required by checker
[33m0cda396[m Fix DetailView import to use 'from django.views.generic.detail import DetailView'
[33m7c00744[m Update urls.py to include exact patterns: add_book/ and edit_book/ as required by checker
[33m2e3bb0c[m Fix permission_required import to be on separate line as required by checker
[33mf9c3fb7[m Extend Book model with custom permissions and implement permission-secured views for book operations
[33m853e2c4[m Extend User model with UserProfile roles and implement role-based views with access control
[33m3e483ff[m Fix urls.py to include exact patterns: views.register, LoginView.as_view(), LogoutView.as_view() with template names
[33m3713ebb[m Add user authentication features to relationship_app with login, logout, and registration
[33mb270cf7[m Fix urls.py import to include 'from .views import list_books'
[33m83ab449[m Fix DetailView import to use 'from django.views.generic.detail import DetailView'
[33mee31082[m Fix views.py import to include 'from .models import Library' for class-based view
[33m8fd7aaa[m Fix views.py imports to use 'from django.views.generic.detail import DetailView'
[33ma730d6a[m Fix views.py import to include 'from .models import Library' for class-based view
[33m70bc30f[m Fix views.py import to include 'from .models import Library' for class-based view
[33mf33ffbe[m Complete relationship_app views with function-based and class-based implementations
[33m692a4e4[m Update query_samples.py with Librarian.objects.get(library__name=) pattern
[33me03359d[m Fix relationship_app location and configuration
[33m80fe2e1[m Add django-models directory with relationship_app showcasing complex model relationships
[33m6d19307[m Enhance bookshelf app: integrate Book model with Django admin interface
[33md04c392[m Fix file locations: move CRUD documentation to bookshelf app directory
[33m18fe580[m Add bookshelf app with complete CRUD documentation
[33m389cabb[m Correct project structure: manage.py and README.md both in LibraryProject directory
[33mc246533[m Initial Django project setup: LibraryProject
