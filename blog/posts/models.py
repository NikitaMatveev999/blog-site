from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_likes')
    favourite = models.ManyToManyField(User, related_name='favourite')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.text
