from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, like_view,\
    favourite_view, SearchResultsView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('add_post/', PostCreateView.as_view(), name='add_post'),
    path('post/update_post/<int:pk>', PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='delete_post'),
    path('like/<int:pk>', like_view, name='like_post'),
    path('favourite/<int:pk>', favourite_view, name='favourite_post'),
    path('search/', SearchResultsView.as_view(), name='search_results')
]
