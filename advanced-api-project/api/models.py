from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    Fields:
    - name: CharField storing the author's full name
    """
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing a published book.
    
    Fields:
    - title: CharField storing the book's title
    - publication_year: IntegerField storing the year of publication
    - author: ForeignKey linking to the Author model (one-to-many relationship)
    
    Relationship:
    - One Author can have multiple Books (one-to-many)
    - Each Book has exactly one Author
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,  # Delete books when author is deleted
        related_name='books'  # Enables author.books.all() to get all books by author
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']
        unique_together = ['title', 'author']  # Prevent duplicate books by same author
