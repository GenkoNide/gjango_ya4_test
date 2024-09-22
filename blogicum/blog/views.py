from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from .models import Post, Category
from .constants import MAX_BLOGS_PER_CATEGORY


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        pub_date__date__lt=timezone.now(),
        is_published=True,
        category__is_published=True
    )[:MAX_BLOGS_PER_CATEGORY]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post_detail = get_object_or_404(Post, pk=id,
                                    is_published=True,
                                    category__is_published=True,
                                    pub_date__date__lt=timezone.now())
    context = {'post': post_detail}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category,
                                 is_published=True,
                                 slug=category_slug)
    post_list = Post.objects.filter(pub_date__date__lt=timezone.now(),
                                    category=category,
                                    is_published=True)
    context = {'category': category,
               'post_list': post_list}
    return render(request, template, context)


def create_post(request):
    template = 'blog/create_post.html'
    category = get_object_or_404(Category, is_published=True)
    return render(request, template, {'category': category})


def edit_post(request, id):
    template = 'blog/edit_post.html'
    return render(request, template, {'post': get_object_or_404(Post, pk=id)})


def delete_post(request, id):
    template = 'blog/delete_post.html'
    return render(request, template, {'post': get_object_or_404(Post, pk=id)})


def profile(request, id):
    template = 'blog/profile.html'
    post = get_object_or_404(Post, pk=id)
    context = {'post': post}
    return render(request, template, context)
