# Posts and Comments API Documentation

## Posts Endpoints

### List Posts
**GET** `/api/posts/`

**Query Parameters:**
- `page` - Page number for pagination
- `search` - Search in title and content
- `author` - Filter by author ID
- `ordering` - Sort by fields (created_at, updated_at, like_count)

**Response:**
```json
{
    "count": 100,
    "next": "http://api.example.com/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": {
                "id": 1,
                "username": "johndoe",
                "profile_picture": "/media/profile_pics/default.jpg"
            },
            "title": "My First Post",
            "content": "This is my first post content...",
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z",
            "like_count": 5,
            "comment_count": 3,
            "is_liked": false,
            "comments": []
        }
    ]
}
