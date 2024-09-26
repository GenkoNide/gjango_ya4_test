from django.urls import path, include

from .views import PostDetailView, PostCategoryView, PostCreateView, PostEditView, PostDeleteView, MainPageView, \
    CommentCreateView, CommentUpdateView, CommentDeleteView

app_name = 'blog'

urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('posts/<int:pk>/',PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:post_id>/edit', PostEditView.as_view(), name='edit_post'),
    path('posts/<int:post_id>/delete', PostDeleteView.as_view, name='delete_post'),
    path('posts/<int:post_id>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/', CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/', CommentDeleteView.as_view(), name='delete_comment'),
    path('category/<slug:category_slug>/',PostCategoryView.as_view(), name='category_posts'),
    path('profile/', include('users.urls')),
]
