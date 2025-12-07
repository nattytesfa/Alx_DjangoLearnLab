# Blog Post Management Documentation

## Overview
The Django Blog project provides comprehensive CRUD (Create, Read, Update, Delete) operations for blog posts. This system allows authenticated users to create, edit, and delete their posts while providing public access to read posts.

## Features

### 1. Public Access Features
- **Browse All Posts**: View all blog posts with pagination
- **Search Posts**: Search by title, content, or author
- **View Post Details**: Read complete posts with comments
- **Filter by Author**: View posts by specific authors

### 2. Authenticated User Features
- **Create Posts**: Write and publish new blog posts
- **Edit Posts**: Update existing posts (author only)
- **Delete Posts**: Remove posts permanently (author only)
- **Manage Comments**: View and approve comments on posts

## CRUD Operations

### CREATE (Post Creation)
**URL**: `/post/new/`
**Access**: Authenticated users only
**Features**:
- Rich text editor with formatting tools
- Title and content validation
- Automatic author assignment
- Live preview option
- Character counters

### READ (Post Viewing)
**URLs**:
- List: `/posts/` (all posts)
- Detail: `/post/<id>/` (single post)

**Access**: Public
**Features**:
- Paginated post listings
- Search functionality
- Post excerpts
- Author information
- Comment sections

### UPDATE (Post Editing)
**URL**: `/post/<id>/update/`
**Access**: Post author or superuser only
**Features**:
- Full editing capabilities
- Original post preservation
- Edit confirmation
- Access control

### DELETE (Post Removal)
**URL**: `/post/<id>/delete/`
**Access**: Post author or superuser only
**Features**:
- Double confirmation
- Warning about permanence
- Comment deletion cascade
- Success notification

## Permission System

### Access Control Levels:
1. **Public Users**:
   - View post lists
   - Read individual posts
   - View approved comments

2. **Authenticated Users**:
   - All public access
   - Create new posts
   - Edit own posts
   - Delete own posts
   - Add comments

3. **Superusers**:
   - All authenticated user access
   - Edit any post
   - Delete any post
   - Moderate comments
   - Access admin panel

### Security Features:
- CSRF protection on all forms
- Permission checks on sensitive operations
- Input validation and sanitization
- Secure session management
- Author-only access enforcement

## Templates

### 1. `post_list.html`
- Displays paginated list of posts
- Search bar functionality
- Author filtering
- Post excerpts with "Read More" links

### 2. `post_detail.html`
- Full post display
- Author information
- Comment section
- Edit/Delete buttons (author only)

### 3. `post_form.html`
- Create/Edit post form
- Rich text editor
- Live preview
- Character counters
- Formatting toolbar

### 4. `post_confirm_delete.html`
- Delete confirmation
- Post preview
- Warning messages
- Double verification

## Forms

### `PostForm`
**Fields**:
- `title`: CharField (max 200 chars, required)
- `content`: TextField (required)

**Validation**:
- Title: 5-200 characters, not empty
- Content: Minimum 10 characters, not empty
- Auto-trim whitespace

**Features**:
- Bootstrap styling
- Character counters
- Rich text formatting hints

## Views

### Class-Based Views:
1. **PostListView**: List all posts (public)
2. **PostDetailView**: Show single post (public)
3. **PostCreateView**: Create post (authenticated)
4. **PostUpdateView**: Edit post (author only)
5. **PostDeleteView**: Delete post (author only)

### Mixins Used:
- `LoginRequiredMixin`: For create, update, delete
- `UserPassesTestMixin`: For author verification

## URL Patterns

- /posts/ # List all posts
- /post/new/ # Create new post
- /post/int:pk/ # View post details
- /post/int:pk/update/ # Edit post
- /post/int:pk/delete/ # Delete post


## Testing Guide

### Manual Testing Scenarios:

1. **Create Post Test**:
   ```bash
   # Login → Navigate to /post/new/ → Fill form → Submit
   # Expected: Post created, redirect to post detail, success message

2. **Edit Post Test**:
# View post → Click Edit → Modify content → Submit
# Expected: Post updated, success message

3. **Delete Post Test**:
# View post → Click Delete → Confirm → Submit
# Expected: Post deleted, redirect to list, success message

4. **Permission Test**:
# Try editing/deleting other user's post
# Expected: Permission denied, error message

5. **Search Test**:
# Navigate to /posts/ → Enter search term
# Expected: Filtered results


