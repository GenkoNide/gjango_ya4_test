from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView)

from blog.forms import PostForm, CommentForm
from .models import Post, Category, Comment
from .constants import POST_AMOUNT


class MainPageView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = POST_AMOUNT

    def get_queryset(self):
        return Post.objects.filter(is_published=True,
                                   category__is_published=True,
                                   pub_date__lte=timezone.now()).order_by('-pub_date')


class PostCategoryView(ListView):
    model = Category
    template_name = 'blog/category.html'
    category = None
    paginate_by = POST_AMOUNT

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category,
                                          slug=kwargs['category_slug'],
                                          is_published=True)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(is_published=True,
                                   category=self.category.id,
                                   pub_date__lte=timezone.now()).order_by('-pub_date')


class PostDetailView(DetailView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        if post.author != self.request.user and not post.is_published:
            raise Http404
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.prefetch_related('post').filter(post=post)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'username': self.object.pk})


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user and not self.request.user.is_superuser:
            return redirect('blog:post_detail', self.kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs.get('post_id')})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/create.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user and not self.request.user.is_superuser:
            return redirect('blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')})
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    comment = None

    def get_object(self, **kwargs):
        return get_object_or_404(Comment, pk=self.kwargs.get('comment_id'),
                                 post=Post.objects.get(pk=self.kwargs.get('post_id')), author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        self.comment = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs.get('post_id')})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Comment, pk=self.kwargs.get('comment_id'), post=self.kwargs.get('post_id'),
                                 author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs.get('post_id')})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_object(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404
        return get_object_or_404(Comment, pk=self.kwargs.get('comment_id'), post=self.kwargs.get('post_id'),
                                 author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user and not self.request.user.is_superuser:
            return redirect('blog:post_detail', post_id=self.get_object().id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs.get('post_id')})
