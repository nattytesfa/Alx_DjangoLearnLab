from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.db.models import Q
from django.utils import timezone
from .models import Post, Comment
from .forms import UserRegisterForm, UserUpdateForm, PostForm


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
    Accessible to all users.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.all().order_by('-published_date')
        
        # Filter by author if requested
        author_id = self.request.GET.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        
        # Add statistics for the template
        if self.request.user.is_authenticated:
            context['user_post_count'] = Post.objects.filter(
                author=self.request.user
            ).count()
        
        return context


class PostDetailView(DetailView):
    """
    View for displaying a single blog post.
    Accessible to all users.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get approved comments or all if user is superuser
        if self.request.user.is_superuser:
            comments = post.comments.all()
        else:
            comments = post.comments.filter(approved_comment=True)
        
        context['comments'] = comments
        
        # Check if user can edit/delete this post
        if self.request.user.is_authenticated:
            context['can_edit'] = (
                post.author == self.request.user or 
                self.request.user.is_superuser
            )
        
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new blog post.
    Only accessible to authenticated users.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        response = super().form_valid(form)
        
        messages.success(
            self.request, 
            f'Your post "{form.instance.title}" has been published successfully!'
        )
        return response
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing blog post.
    Only accessible to the post author or superuser.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        """
        Test if user is the author or superuser.
        """
        post = self.get_object()
        return (
            self.request.user == post.author or 
            self.request.user.is_superuser
        )
    
    def handle_no_permission(self):
        """
        Handle unauthorized access attempts.
        """
        messages.error(self.request, 'You are not authorized to edit this post.')
        return redirect('post-detail', pk=self.kwargs['pk'])
    
    def form_valid(self, form):
        messages.success(
            self.request, 
            f'Your post "{form.instance.title}" has been updated successfully!'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a blog post.
    Only accessible to the post author or superuser.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def test_func(self):
        """
        Test if user is the author or superuser.
        """
        post = self.get_object()
        return (
            self.request.user == post.author or 
            self.request.user.is_superuser
        )
    
    def handle_no_permission(self):
        """
        Handle unauthorized access attempts.
        """
        messages.error(self.request, 'You are not authorized to delete this post.')
        return redirect('post-detail', pk=self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):
        """
        Override delete to add success message.
        """
        post = self.get_object()
        messages.success(
            request, 
            f'Post "{post.title}" has been deleted successfully.'
        )
        return super().delete(request, *args, **kwargs)


class UserRegisterView(CreateView):
    """
    View for user registration.
    """
    form_class = UserRegisterForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'Account created successfully! Welcome, {user.username}!')
        return redirect(self.success_url)


class UserProfileView(LoginRequiredMixin, UpdateView):
    """
    View for user profile management.
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'blog/profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated!')
        return super().form_valid(form)


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
