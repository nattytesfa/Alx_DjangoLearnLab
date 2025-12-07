# Comment System Documentation

## Overview
The Django Blog comment system provides a comprehensive platform for users to engage with blog posts through comments and replies. The system includes full CRUD operations with proper permissions and moderation capabilities.

## Features

### 1. Comment Features
- **Read Comments**: All users can view approved comments
- **Create Comments**: Authenticated users can post comments
- **Edit Comments**: Authors can edit their own comments
- **Delete Comments**: Authors, post authors, and superusers can delete comments
- **Reply to Comments**: Nested comment replies
- **Comment Moderation**: Post authors and superusers can approve/unapprove comments

### 2. Security & Permissions
- **CSRF Protection**: All comment forms protected
- **Permission-Based Access**: Role-based comment management
- **Input Validation**: Content length and format validation
- **Moderation System**: Comment approval workflow

## Models

### Comment Model Fields:
- `post`: ForeignKey to Post (required)
- `author`: ForeignKey to User (required)
- `content`: TextField (1000 char limit)
- `created_at`: DateTimeField (auto-created)
- `updated_at`: DateTimeField (auto-updated)
- `approved`: BooleanField (default: True)
- `parent`: ForeignKey to self (for nested replies)

## Views

### Comment Views:
1. **CommentCreateView**: Create new comments
2. **CommentUpdateView**: Edit existing comments
3. **CommentDeleteView**: Delete comments
4. **comment_reply_view**: Reply to specific comments
5. **toggle_comment_approval**: Moderate comment approval

### Permission Mixins:
- `LoginRequiredMixin`: For create, update, delete
- `UserPassesTestMixin`: For author verification

## Forms

### 1. CommentForm
- **Purpose**: Create new comments
- **Fields**: `content`, `parent` (hidden)
- **Validation**: 5-1000 characters, not empty

### 2. CommentEditForm
- **Purpose**: Edit existing comments
- **Fields**: `content`
- **Features**: Character counter, edit indicator

## URL Patterns
- /post/int:post_id/comment/new/ # Create comment
- /post/int:post_id/comment/int:parent_id/reply/ # Reply to comment
- /comment/int:pk/edit/ # Edit comment
- /comment/int:pk/delete/ # Delete comment
- /comment/int:comment_id/toggle-approval/ # Toggle approval


## Templates

### 1. Comment Display Templates:
- `comment_item.html`: Individual comment display with actions
- Integrated into `post_detail.html` for comment listing

### 2. Comment Action Templates:
- `comment_form.html`: Create new comment
- `comment_edit_form.html`: Edit existing comment
- `comment_reply_form.html`: Reply to comment
- `comment_confirm_delete.html`: Delete confirmation

## JavaScript Features

### Interactive Elements:
1. **Character Counters**: Real-time character counting
2. **Reply Forms**: Toggle reply forms on demand
3. **Form Validation**: Client-side validation
4. **Confirmation Dialogs**: Delete confirmation
5. **Dynamic Updates**: AJAX form submission support

## Testing Guide

### Manual Testing Scenarios:

1. **Create Comment**:
   - Login → View post → Add comment → Submit
   - Expected: Comment appears, success message

2. **Edit Comment**:
   - View own comment → Edit → Modify → Submit
   - Expected: Comment updated, "edited" indicator

3. **Delete Comment**:
   - View own comment → Delete → Confirm
   - Expected: Comment removed, success message

4. **Reply to Comment**:
   - View comment → Reply → Write reply → Submit
   - Expected: Nested reply appears

5. **Moderate Comment**:
   - As post author/superuser → Toggle approval
   - Expected: Comment approval status changes

### Permission Tests:
- Unauthenticated users cannot post/edit/delete
- Users cannot edit/delete others' comments
- Post authors can moderate comments
- Superusers have all permissions


