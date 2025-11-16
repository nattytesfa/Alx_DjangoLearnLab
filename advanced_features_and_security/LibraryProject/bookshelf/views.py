from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Book, Author
from django import forms
from .forms import ExampleForm, SecureBookForm


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """View to list all books - requires can_view permission"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """View to create a new book - requires can_create permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    """View to edit a book - requires can_edit permission"""
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    """View to delete a book - requires can_delete permission"""
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


def example_form_view(request):
    """
    Security: Example view demonstrating secure form handling
    Shows proper CSRF protection and input validation
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Security: Form data is now validated and sanitized
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Security: Success message with escaped data
            messages.success(
                request, 
                f'Thank you {name}! Your message has been received securely.'
            )
            
            # In a real application, you would save to database here
            # Security: Always use validated form.cleaned_data
            
            return render(request, 'bookshelf/form_success.html', {
                'name': name,
                'email': email,
            })
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})

@login_required
def secure_form_demo(request):
    """
    Security: Demonstration of secure form practices
    """
    if request.method == 'POST':
        form = SecureBookForm(request.POST)
        if form.is_valid():
            # Security: The form instance is ready to be saved
            book = form.save(commit=False)
            # Additional security: Any additional processing here
            book.save()
            messages.success(request, 'Book created securely!')
            return redirect('bookshelf:book_list')
    else:
        form = SecureBookForm()
    
    return render(request, 'bookshelf/secure_form_demo.html', {'form': form})

