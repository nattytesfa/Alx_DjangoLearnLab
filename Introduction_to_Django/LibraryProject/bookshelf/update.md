# Update Operation

## Command:
\`\`\`python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Verify the update
updated_book = Book.objects.get(id=book.id)
print(f"Updated title: {updated_book.title}")
\`\`\`

## Expected Output:
\`\`\`python
Updated title: Nineteen Eighty-Four
\`\`\`
