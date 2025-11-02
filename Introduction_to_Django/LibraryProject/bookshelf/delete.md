# Delete Operation

## Command:
\`\`\`python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion
all_books = Book.objects.all()
print(f"Books in database: {all_books.count()}")
\`\`\`

## Expected Output:
\`\`\`python
Books in database: 0
\`\`\`
