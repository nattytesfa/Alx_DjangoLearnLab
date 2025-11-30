import os
import django
import requests

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

BASE_URL = 'http://127.0.0.1:8002/api/'

def test_advanced_queries():
    print("Testing Advanced Query Capabilities...")
    
    # Test 1: Basic filtering by publication_year
    print("\n1. Testing Filtering by publication_year...")
    response = requests.get(BASE_URL + 'books/?publication_year=1997')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"✓ Found {len(books)} books from 1997")
    
    # Test 2: Filtering by author
    print("\n2. Testing Filtering by author...")
    response = requests.get(BASE_URL + 'books/?author=1')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"✓ Found {len(books)} books by author ID 1")
    
    # Test 3: Search functionality
    print("\n3. Testing Search functionality...")
    response = requests.get(BASE_URL + 'books/?search=harry')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"✓ Search found {len(books)} results for 'harry'")
    
    # Test 4: Ordering by title
    print("\n4. Testing Ordering by title...")
    response = requests.get(BASE_URL + 'books/?ordering=title')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"✓ Ordered {len(books)} books by title")
    
    # Test 5: Ordering by publication_year (descending)
    print("\n5. Testing Ordering by publication_year (descending)...")
    response = requests.get(BASE_URL + 'books/?ordering=-publication_year')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        if len(books) > 1:
            # Check if properly ordered (newest first)
            years = [book['publication_year'] for book in books]
            is_descending = all(years[i] >= years[i+1] for i in range(len(years)-1))
            print(f"✓ Descending order: {is_descending}")
    
    # Test 6: Combined filtering and ordering
    print("\n6. Testing Combined filtering and ordering...")
    response = requests.get(BASE_URL + 'books/?publication_year=1997&ordering=title')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"✓ Combined query found {len(books)} results")
    
    # Test 7: Search with author name
    print("\n7. Testing Search by author name...")
    response = requests.get(BASE_URL + 'books/?search=rowling')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"✓ Search found {len(books)} results for author 'rowling'")
    
    # Test 8: Custom range filtering (if implemented)
    print("\n8. Testing Custom range filtering...")
    response = requests.get(BASE_URL + 'books/?min_year=1900&max_year=2000')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"✓ Range filtering found {len(books)} results")
    
    print("\n🎉 All advanced query tests completed!")

if __name__ == "__main__":
    test_advanced_queries()
