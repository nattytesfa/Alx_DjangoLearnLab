from django.urls import path
from .views import add_book, edit_book

app_name = 'relationship_app'

urlpatterns = [
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),
]
