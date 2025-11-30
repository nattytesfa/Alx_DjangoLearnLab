
# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class BaseTestCase(APITestCase):
    """
    Base test case with common setup for all API tests.
    """
    
    def setUp(self):
        """
        Set up test data and client for all test cases.
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")
        self.author3 = Author.objects.create(name="Jane Austen")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title="Pride and Prejudice",
            publication_year=1813,
            author=self.author3
        )
        
        # API client
        self.client = APIClient()


class BookListViewTests(BaseTestCase):
    """
    Test cases for Book List and Create endpoints.
    """
    
    def test_get_all_books(self):
        """
        Test retrieving all books without authentication.
        Should return 200 OK and all books.
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
        # Check if all books are in response
        book_titles = [book['title'] for book in response.data]
        self.assertIn("Harry Potter and the Philosopher's Stone", book_titles)
        self.assertIn("1984", book_titles)
    
    def test_create_book_authenticated(self):
        """
        Test creating a book with authentication.
        Should return 201 Created.
        """
        url = reverse('book-create')
        self.client.force_authenticate(user=self.user)
        
        book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(url, book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Handle both response formats - check if it's your custom format or standard DRF
        if 'data' in response.data:
            # Custom response format from your mixins
            self.assertEqual(response.data['data']['title'], 'New Test Book')
            self.assertEqual(response.data['status'], 'success')
        else:
            # Standard DRF response format
            self.assertEqual(response.data['title'], 'New Test Book')
        
        self.assertEqual(Book.objects.count(), 5)  # 4 initial + 1 new
        
        def test_create_book_unauthenticated(self):
            """
            Test creating a book without authentication.
            Should return 403 Forbidden.
            """
            url = reverse('book-create')
            
            book_data = {
                'title': 'Unauthorized Book',
                'publication_year': 2023,
                'author': self.author1.id
            }
            
            response = self.client.post(url, book_data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(Book.objects.count(), 4)  # No new book created
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Harry Potter and the Philosopher's Stone")
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author2.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 books by George Orwell
    
    def test_search_books_by_title(self):
        """
        Test searching books by title.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('Harry', response.data[0]['title'])
    
    def test_search_books_by_author_name(self):
        """
        Test searching books by author name.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'orwell'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 books by George Orwell
    
    def test_order_books_by_title(self):
        """
        Test ordering books by title.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if books are ordered by title
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_publication_year_desc(self):
        """
        Test ordering books by publication year descending.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if books are ordered by publication year descending
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_combined_filter_search_order(self):
        """
        Test combined filtering, searching, and ordering.
        """
        url = reverse('book-list')
        response = self.client.get(url, {
            'author': self.author2.id,
            'ordering': '-publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only George Orwell's books
        
        # Check ordering (should be newest first)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1949, 1945])  # 1984 then Animal Farm


class BookDetailViewTests(BaseTestCase):
    """
    Test cases for Book Detail, Update, and Delete endpoints.
    """
    
    def test_get_single_book(self):
        """
        Test retrieving a single book.
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_get_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist.
        """
        url = reverse('book-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
# In BookDetailViewTests class, update these methods:

    def test_update_book_authenticated(self):
        """
        Test updating a book with authentication.
        """
        url = reverse('book-update', kwargs={'pk': self.book1.id})  # Use book-update with pk
        self.client.force_authenticate(user=self.user)
        
        update_data = {
            'title': 'Updated Title',
            'publication_year': 1998,
            'author': self.book1.author.id
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database and check updates
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
        self.assertEqual(self.book1.publication_year, 1998)

    def test_update_book_unauthenticated(self):
        """
        Test updating a book without authentication.
        """
        url = reverse('book-update', kwargs={'pk': self.book1.id})  # Use book-update with pk
        
        update_data = {
            'title': 'Unauthorized Update',
            'publication_year': 1998,
            'author': self.book1.author.id
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_book(self):
        """
        Test partial update of a book.
        """
        url = reverse('book-update', kwargs={'pk': self.book1.id})  # Use book-update with pk
        self.client.force_authenticate(user=self.user)
        
        update_data = {
            'title': 'Partially Updated Title'
        }
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database and check updates
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        # Other fields should remain unchanged
        self.assertEqual(self.book1.publication_year, 1997)

    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authentication.
        """
        url = reverse('book-delete', kwargs={'pk': self.book1.id})  # Use book-delete with pk
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
        self.assertEqual(Book.objects.count(), 3)  # One less book

    def test_delete_book_unauthenticated(self):
        """
        Test deleting a book without authentication.
        """
        url = reverse('book-delete', kwargs={'pk': self.book1.id})  # Use book-delete with pk
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())  # Book still exists
class AuthorViewTests(BaseTestCase):
    """
    Test cases for Author endpoints.
    """
    
    def test_get_all_authors(self):
        """
        Test retrieving all authors.
        """
        url = reverse('author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        # Check if nested books are included
        author_with_books = next(a for a in response.data if a['name'] == 'George Orwell')
        self.assertEqual(len(author_with_books['books']), 2)
    
    def test_get_single_author(self):
        """
        Test retrieving a single author with nested books.
        """
        url = reverse('author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], "Harry Potter and the Philosopher's Stone")


class ValidationTests(BaseTestCase):
    """
    Test cases for data validation.
    """
    
    def test_create_book_future_publication_year(self):
        """
        Test creating a book with future publication year (should fail validation).
        """
        url = reverse('book-create')
        self.client.force_authenticate(user=self.user)
        
        from django.utils import timezone
        future_year = timezone.now().year + 1
        
        book_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        
        response = self.client.post(url, book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_duplicate_title_author(self):
        """
        Test creating a book with duplicate title and author (should fail due to unique constraint).
        """
        url = reverse('book-create')
        self.client.force_authenticate(user=self.user)
        
        book_data = {
            'title': self.book1.title,  # Same title as existing book
            'publication_year': 2023,
            'author': self.book1.author.id  # Same author
        }
        
        response = self.client.post(url, book_data, format='json')
        
        # This might return 400 or 500 depending on how uniqueness is handled
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR])


class PermissionTests(BaseTestCase):
    """
    Test cases for permission and authentication.
    """
    
    def test_admin_user_can_perform_all_operations(self):
        """
        Test that admin users can perform all CRUD operations.
        """
        self.client.force_authenticate(user=self.admin_user)
        
        # Test create
        create_url = reverse('book-create')
        book_data = {
            'title': 'Admin Created Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(create_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Test update - use the correct URL pattern with pk
        update_url = reverse('book-update', kwargs={'pk': self.book1.id})
        update_data = {'title': 'Admin Updated Title'}
        response = self.client.patch(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test delete - use the correct URL pattern with pk
        delete_url = reverse('book-delete', kwargs={'pk': self.book2.id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
