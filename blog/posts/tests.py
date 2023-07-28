from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Post


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            author=self.user,
            body='Test Content',
            category=self.category
        )
        self.user.favourite.add(self.post)

    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/index.html')
        self.assertContains(response, 'Test Post')

    def test_registration_view(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')

    def test_post_detail_view(self):
        url = reverse('detail', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/detail.html')
        self.assertContains(response, 'Test Post')

    def test_favourite_list_view(self):
        self.client.force_login(self.user)
        url = reverse('favourite_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/favourite.html')
        self.assertContains(response, 'Test Post')

    def test_add_like_view(self):
        self.client.force_login(self.user)
        url = reverse('like_post', args=[self.post.pk])
        response = self.client.post(url, {'post_id': self.post.pk})
        self.assertEqual(response.status_code, 302)

        self.post.refresh_from_db()
        self.assertEqual(self.post.likes.count(), 1)

        response = self.client.post(url, {'post_id': self.post.pk})
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes.count(), 0)

    def test_post_create_view(self):
        self.client.force_login(self.user)
        url = reverse('add_post')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/add_post.html')

    def test_post_update_view(self):
        self.client.force_login(self.user)
        url = reverse('update_post', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/update_post.html')

    def test_post_delete_view(self):
        self.assertEqual(self.post.author, self.user)

        url = reverse('delete_post', args=[self.post.pk])
        response = self.client.get(url)
        if self.post.author == self.user:
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'posts/delete_post.html')
        else:
            self.assertIn(response.status_code, [403, 404])
        self.client.force_login(self.user)
        url = reverse('delete_post', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/delete_post.html')

    def test_search_results_view(self):
        url = reverse('search_results')
        response = self.client.get(url, {'q': 'Test Content'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/search_results.html')
        self.assertContains(response, 'Test Post')

    def test_category_view(self):
        url = reverse('category', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/categories.html')
        self.assertContains(response, 'Test Post')

    def test_add_favourite_view(self):
        self.client.force_login(self.user)
        url = reverse('favourite_post', args=[self.post.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.post.refresh_from_db()
        self.assertFalse(self.post.favourite.filter(id=self.user.id).exists())

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertTrue(self.post.favourite.filter(id=self.user.id).exists())
