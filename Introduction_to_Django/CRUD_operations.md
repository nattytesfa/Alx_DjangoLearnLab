# CRUD Operations Documentation

## 1. Create Operation
\`\`\`python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Created: {book.title} by {book.author} ({book.publication_year})")
\`\`\`
**Output:**
\`\`\`
Created: 1984 by George Orwell (1949)
\`\`\`

## 2. Retrieve Operation
\`\`\`python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
\`\`\`
**Output:**
\`\`\`
Title: 1984
Author: George Orwell
Publication Year: 1949
\`\`\`

## 3. Update Operation
\`\`\`python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

updated_book = Book.objects.get(id=book.id)
print(f"Updated title: {updated_book.title}")
\`\`\`
**Output:**
\`\`\`
Updated title: Nineteen Eighty-Four
\`\`\`

## 4. Delete Operation
\`\`\`python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

all_books = Book.objects.all()
print(f"Books in database: {all_books.count()}")
\`\`\`
**Output:**
\`\`\`
Books in database: 0
\`\`\`
