from django.shortcuts import render

# Create your views here.from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post, Comment


def home(request):
    """
    Home page view.
    """
    recent_posts = Post.objects.all().order_by('-published_date')[:3]
    return render(request, 'blog/home.html', {
        'recent_posts': recent_posts
    })


class PostListView(ListView):
    """
    View for listing all blog posts.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        return Post.objects.all().order_by('-published_date')


class PostDetailView(DetailView):
    """
    View for displaying a single blog post.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new blog post.
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing blog post.
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user is the author or superuser
        obj = self.get_object()
        if obj.author != request.user and not request.user.is_superuser:
            messages.error(request, 'You are not authorized to edit this post.')
            return redirect('post-detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a blog post.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user is the author or superuser
        obj = self.get_object()
        if obj.author != request.user and not request.user.is_superuser:
            messages.error(request, 'You are not authorized to delete this post.')
            return redirect('post-detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)


@login_required
def add_comment(request, pk):
    """
    View for adding a comment to a post.
    """
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        
        if content:
            comment = Comment(
                post=post,
                author=request.user,
                content=content,
                approved_comment=not request.user.is_superuser  # Auto-approve for superusers
            )
            comment.save()
            
            if comment.approved_comment:
                messages.success(request, 'Comment added successfully!')
            else:
                messages.info(request, 'Comment submitted for approval.')
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    return redirect('post-detail', pk=post.pk)
