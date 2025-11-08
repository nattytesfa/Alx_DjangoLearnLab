from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library

def list_books(request):
    from .models import Book
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    from .models import Library
    model = Library
    template_name = 'relationship_app/library_detail.html'
