from django.contrib import admin
from .models import UserProfile, Author, Book, Library, Librarian

# UserProfile Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__email', 'user__username']

# Register models
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
