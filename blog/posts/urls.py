from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView


urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('add_post/', PostCreateView.as_view(), name='add_post'),
    path('post/update_post/<int:pk>', PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='delete_post')
]