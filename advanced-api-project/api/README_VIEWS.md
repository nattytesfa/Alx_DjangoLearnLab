# API Views Documentation

## Generic Views Implementation

### Book Views
- `BookListView`: List all books with filtering/searching (GET /api/books/)
- `BookDetailView`: Retrieve single book (GET /api/books/<id>/)
- `BookCreateView`: Create new book (POST /api/books/create/) - Requires auth
- `BookUpdateView`: Update book (PUT/PATCH /api/books/<id>/update/) - Requires auth
- `BookDeleteView`: Delete book (DELETE /api/books/<id>/delete/) - Requires auth

### Author Views
- `AuthorListView`: List all authors with books (GET /api/authors/)
- `AuthorDetailView`: Retrieve single author with books (GET /api/authors/<id>/)

## Permission Classes
- `AllowAny`: Public read access
- `IsAuthenticated`: Required for write operations
- `IsAuthenticatedOrReadOnly`: Read for all, write for authenticated
- `IsAdminOrReadOnly`: Read for all, write for admin only

## Features
- Filtering by publication_year and author
- Search by book title and author name
- Ordering by multiple fields
- Custom response formats for create/update/delete
- Comprehensive error handling
