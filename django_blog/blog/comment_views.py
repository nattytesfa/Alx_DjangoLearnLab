from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from .models import Post, Comment
from .forms import CommentForm, CommentEditForm


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new comment.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return context
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        
        # Handle parent comment for replies
        parent_id = self.request.POST.get('parent')
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id, post=post)
                form.instance.parent = parent_comment
            except Comment.DoesNotExist:
                pass
        
        response = super().form_valid(form)
        
        messages.success(
            self.request,
            'Your comment has been posted successfully!'
        )
        
        # Return JSON for AJAX requests
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Comment posted successfully',
                'comment_id': self.object.id,
                'redirect_url': self.get_success_url()
            })
        
        return response
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['post_id']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing comment.
    Only accessible to the comment author or superuser.
    """
    model = Comment
    form_class = CommentEditForm
    template_name = 'blog/comment_edit_form.html'
    
    def test_func(self):
        """
        Test if user can edit this comment.
        """
        comment = self.get_object()
        return comment.can_edit(self.request.user)
    
    def handle_no_permission(self):
        """
        Handle unauthorized access attempts.
        """
        messages.error(self.request, 'You are not authorized to edit this comment.')
        return redirect('post-detail', pk=self.get_object().post.pk)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        messages.success(
            self.request,
            'Your comment has been updated successfully!'
        )
        
        # Return JSON for AJAX requests
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Comment updated successfully',
                'comment_id': self.object.id,
                'content': self.object.content,
                'is_edited': self.object.is_edited(),
                'updated_at': self.object.updated_at.strftime('%B %d, %Y %H:%M')
            })
        
        return response
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a comment.
    Accessible to comment author, post author, or superuser.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        """
        Test if user can delete this comment.
        """
        comment = self.get_object()
        return comment.can_delete(self.request.user)
    
    def handle_no_permission(self):
        """
        Handle unauthorized access attempts.
        """
        messages.error(self.request, 'You are not authorized to delete this comment.')
        return redirect('post-detail', pk=self.get_object().post.pk)
    
    def delete(self, request, *args, **kwargs):
        """
        Override delete to handle AJAX requests and add success message.
        """
        self.object = self.get_object()
        post_pk = self.object.post.pk
        
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object.delete()
            return JsonResponse({
                'success': True,
                'message': 'Comment deleted successfully'
            })
        
        # Regular request handling
        self.object.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('post-detail', pk=post_pk)


@login_required
def comment_reply_view(request, post_id, parent_id):
    """
    View for replying to a specific comment.
    """
    post = get_object_or_404(Post, pk=post_id)
    parent_comment = get_object_or_404(Comment, pk=parent_id, post=post)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent = parent_comment
            comment.save()
            
            messages.success(request, 'Your reply has been posted!')
            return redirect('post-detail', pk=post_id)
    else:
        form = CommentForm(initial={'parent': parent_id})
    
    return render(request, 'blog/comment_reply_form.html', {
        'form': form,
        'post': post,
        'parent_comment': parent_comment,
    })


@login_required
def toggle_comment_approval(request, comment_id):
    """
    View for toggling comment approval (superusers and post authors only).
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Check permissions
    if not (request.user.is_superuser or request.user == comment.post.author):
        messages.error(request, 'You are not authorized to moderate this comment.')
        return redirect('post-detail', pk=comment.post.pk)
    
    # Toggle approval status
    comment.approved = not comment.approved
    comment.save()
    
    action = "approved" if comment.approved else "unapproved"
    messages.success(request, f'Comment {action} successfully.')
    
    return redirect('post-detail', pk=comment.post.pk)
