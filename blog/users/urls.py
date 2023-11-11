from django.urls import path, include, re_path
from .views import RegistrationView


urlpatterns = [
    path('users/', RegistrationView.as_view(), name='registration'),
    path('register', RegistrationView.as_view(), name='register'),
    re_path('', include('social_django.urls', namespace='social')),

]