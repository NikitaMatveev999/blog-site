from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('posts.urls')),
    path('', include('contact.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    path('__debug__/', include('debug_toolbar.urls')),

]
