# Advanced API Query Guide

## Available Query Parameters

### Filtering Parameters
- `publication_year` - Exact year filter
- `author` - Filter by author ID
- `min_year` - Minimum publication year (custom)
- `max_year` - Maximum publication year (custom)

### Search Parameter
- `search` - Text search in title and author name fields

### Ordering Parameter
- `ordering` - Sort results by field(s)

## Usage Examples

### Basic Filtering
```http
GET /api/books/?publication_year=1997
GET /api/books/?author=1
GET /api/books/?publication_year=1997&author=1
