from django.urls import path, include, re_path
from .views import UserRegistrationView, auth


urlpatterns = [
    path('users/', UserRegistrationView.as_view(), name='registration'),
    re_path('', include('social_django.urls', namespace='social')),
    path('auth/', auth)

]