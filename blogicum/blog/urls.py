from django.urls import path, include

from .views import PostDetailView, PostCategoryView, PostCreateView, PostEditView, PostDeleteView, MainPageView

app_name = 'blog'

urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('posts/<int:id>/',
         PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:post_id>/edit', PostEditView.as_view(), name='post_edit'),
    path('post/<int:post_id>/delete', PostDeleteView.as_view, name='post_delete'),
    path('category/<slug:category_slug>/',
         PostCategoryView.as_view(), name='post_category'),
    path('profile/', include('users.urls')),
]
