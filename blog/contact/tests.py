from django.test import TestCase, Client
from django.urls import reverse
from .models import Contact


class ContactCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact_form')

    def test_contact_create_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_contact_create_post(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        contact = Contact.objects.first()
        self.assertEqual(contact.name, 'Test User')
        self.assertEqual(contact.email, 'test@example.com')
        self.assertEqual(contact.message, 'This is a test message')
