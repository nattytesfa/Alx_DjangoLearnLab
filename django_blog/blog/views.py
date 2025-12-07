from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.db.models import Q
from .models import Post, Comment
from .forms import UserRegisterForm, UserUpdateForm


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
        return context


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
