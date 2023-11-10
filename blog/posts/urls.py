from django.urls import path, include
from .views import HomeView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, \
    SearchResultsView, FavouriteListView, PostAPIView, RegistrationView, AddFavouriteView, AddLikeView, CategoryView, \
    CommentCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register', RegistrationView.as_view(), name='register'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('add_post/', PostCreateView.as_view(), name='add_post'),
    path('post/update_post/<int:pk>', PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='delete_post'),
    path('like/<int:pk>', AddLikeView.as_view(), name='like_post'),
    path('favourite/<int:pk>', AddFavouriteView.as_view(), name='favourite_post'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('category/<str:cat_id>/', CategoryView.as_view(), name='category'),
    path('favourite/', FavouriteListView.as_view(), name='favourite_list'),
    path('post/<int:pk>/comment_create/', CommentCreateView.as_view(), name='comment_create'),
    path('api/v1/postlist/', PostAPIView.as_view()),
    path('api/v1/drf-auth/', include('rest_framework.urls')),

]
