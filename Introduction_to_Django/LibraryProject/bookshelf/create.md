# Create Operation

## Command:
\`\`\`python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
\`\`\`

## Expected Output:
\`\`\`python
# After creation, the book object is returned
# You can verify with:
print(f"Created: {book.title} by {book.author} ({book.publication_year})")
# Output: Created: 1984 by George Orwell (1949)
\`\`\`
