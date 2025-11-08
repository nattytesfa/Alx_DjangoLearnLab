from django.shortcuts import render
from django.views.generic.detail import DetailView  # Exact import pattern
from .models import Library  # Library import at top level

def list_books(request):
    from .models import Book
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
