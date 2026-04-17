from django.urls import path
from .apps import BlogConfig
from .views import BlogPostListView, BlogPostCreateView, BlogPostDetailView, BlogPostUpdateView, BlogPostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path("", BlogPostListView.as_view(), name="blog_post_list"),
    path("blog_post/add/", BlogPostCreateView.as_view(), name="add_blog_post"),
    path("blog_post/<int:pk>/", BlogPostDetailView.as_view(), name="blog_post_detail"),
    path("blog_post_update/<int:pk>/", BlogPostUpdateView.as_view(), name="blog_post_update"),
    path("blog_post_delete/<int:pk>/", BlogPostDeleteView.as_view(), name="blog_post_delete"),
]